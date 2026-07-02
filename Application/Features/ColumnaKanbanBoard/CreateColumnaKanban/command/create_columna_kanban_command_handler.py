from typing import Optional
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.command import (
    CreateColumnaKanbanCommand,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.dtos import (
    ColumnaKanbanResponseDto,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.mappers import (
    ColumnaKanbanMapper,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.validators import (
    CreateColumnaKanbanValidator,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import ConflictException
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class CreateColumnaKanbanCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = Repository(session, ColumnaKanbanConfiguration)
        self._unit_of_work = UnitOfWork(session)
        self._validator = CreateColumnaKanbanValidator(self._repository)

    async def handle(
        self, command: CreateColumnaKanbanCommand, current_user: CurrentUserDto
    ) -> ColumnaKanbanResponseDto:
        command.nombre = command.nombre.strip().upper()
        await self._validator.validate_nombre(command.nombre)

        model = await self._insert_with_retry(command.nombre, command.posicion, current_user.id)
        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        return ColumnaKanbanMapper.to_response(model, current_user)

    async def _insert_with_retry(
        self, nombre: str, posicion: Optional[int], usuario_alta: str
    ) -> ColumnaKanbanConfiguration:
        for attempt in range(5):
            try:
                if posicion is not None:
                    return await self._insert(nombre, posicion, usuario_alta)
                next_pos = await self._get_next_position()
                return await self._insert(nombre, next_pos, usuario_alta)
            except IntegrityError:
                if attempt == 4:
                    raise
        raise ConflictException("Could not assign position after 5 attempts")

    async def _get_next_position(self) -> int:
        stmt = text("""
            SELECT COALESCE(MAX(posicion), 0) + 1
            FROM amonet_columna_kanban
        """)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def _insert(
        self, nombre: str, posicion: int, usuario_alta: str
    ) -> ColumnaKanbanConfiguration:
        stmt = text("""
            INSERT INTO amonet_columna_kanban (
                id_amonet_columna_kanban, nombre, posicion, activo,
                usuario_alta, fecha_alta, usuario_modifica, fecha_modifica
            )
            VALUES (:id, :nombre, :posicion, true, :usuario_alta, NOW(), NULL, NULL)
            RETURNING *
        """)
        result = await self._session.execute(stmt, {
            "id": str(uuid4()),
            "nombre": nombre,
            "posicion": posicion,
            "usuario_alta": str(usuario_alta),
        })
        row = result.fetchone()
        if row is None:
            raise Exception("Insert failed")
        return self._row_to_model(row)

    def _row_to_model(self, row) -> ColumnaKanbanConfiguration:
        return ColumnaKanbanConfiguration(
            id_amonet_columna_kanban=row.id_amonet_columna_kanban,
            nombre=row.nombre,
            posicion=row.posicion,
            activo=row.activo,
            usuario_alta=row.usuario_alta,
            fecha_alta=row.fecha_alta,
            usuario_modifica=row.usuario_modifica,
            fecha_modifica=row.fecha_modifica,
        )

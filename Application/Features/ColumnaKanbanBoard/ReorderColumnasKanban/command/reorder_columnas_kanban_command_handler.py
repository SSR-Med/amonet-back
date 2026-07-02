from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.dtos import (
    ColumnaKanbanResponseDto,
)
from Application.Features.ColumnaKanbanBoard.CreateColumnaKanban.mappers import (
    ColumnaKanbanLoaderOptions,
    ColumnaKanbanMapper,
)
from Application.Features.ColumnaKanbanBoard.ReorderColumnasKanban.command import (
    ReorderColumnasKanbanCommand,
)
from core.dtos import AuditLogDto, CurrentUserDto
from core.exceptions import ConflictException, NotFoundException
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration
from infrastructure.dataaccess.repository import Repository
from infrastructure.dataaccess.unit_of_work import UnitOfWork
from infrastructure.services import AuditLogger


class ReorderColumnasKanbanCommandHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, ColumnaKanbanConfiguration)
        self._unit_of_work = UnitOfWork(session)
        self._session = session

    async def handle(
        self, command: ReorderColumnasKanbanCommand, current_user: CurrentUserDto
    ) -> list[ColumnaKanbanResponseDto]:
        item_ids = [item.id for item in command.items]

        seen = set()
        for item_id in item_ids:
            if item_id in seen:
                raise ConflictException(f"Duplicate column id: {item_id}")
            seen.add(item_id)

        for item_id in item_ids:
            model = await self._repository.first_or_default(
                lambda q: q.where(ColumnaKanbanConfiguration.id_amonet_columna_kanban == item_id)
            )
            if model is None:
                raise NotFoundException("ColumnaKanban", str(item_id))

        now = datetime.now(timezone.utc)
        str_ids = [str(item.id) for item in command.items]

        clear_stmt = text("""
            UPDATE amonet_columna_kanban
            SET posicion = :temp_val
            WHERE id_amonet_columna_kanban = :col_id
        """)

        temp_val = 99999

        for i, col_id in enumerate(item_ids):
            await self._session.execute(
                clear_stmt,
                {"temp_val": temp_val + i, "col_id": str(col_id)},
            )

        set_stmt = text(f"""
            UPDATE amonet_columna_kanban
            SET posicion = :posicion,
                usuario_modifica = :usuario_modifica,
                fecha_modifica = :fecha_modifica
            WHERE id_amonet_columna_kanban = :col_id
        """)

        for i, item in enumerate(command.items):
            await self._session.execute(
                set_stmt,
                {
                    "posicion": item.posicion,
                    "col_id": str(item.id),
                    "usuario_modifica": str(current_user.id),
                    "fecha_modifica": now,
                },
            )

        await self._unit_of_work.commit()

        AuditLogger.log(AuditLogDto(
            usuario=current_user.documento,
            feature=type(self).__name__,
            datos=command.model_dump(),
        ))

        result = []
        for item in command.items:
            updated = await self._repository.first_or_default(
                lambda q: q.where(ColumnaKanbanConfiguration.id_amonet_columna_kanban == item.id),
                loader_options=ColumnaKanbanLoaderOptions.get(),
            )
            if updated is not None:
                result.append(ColumnaKanbanMapper.to_response(updated))

        return result

from typing import Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.TareaSprint.CreateTareaSprint.mappers import (
    TareaSprintLoaderOptions,
    TareaSprintMapper,
)
from Application.Features.TareaSprint.GetTareasBySprint.dtos import (
    ColumnaConTareasDto,
    ColumnaInfoDto,
)
from infrastructure.dataaccess.configurations import (
    ColumnaKanbanConfiguration,
    TareaSprintConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetTareasBySprintQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._tarea_repository = Repository(session, TareaSprintConfiguration)
        self._columna_repository = Repository(session, ColumnaKanbanConfiguration)
        self._session = session

    async def _collect_tag_ids(self, tareas: List[TareaSprintConfiguration]) -> List[UUID]:
        ids: set = set()
        for t in tareas:
            if t.tags:
                for tag_id in t.tags:
                    ids.add(UUID(tag_id) if isinstance(tag_id, str) else tag_id)
        return list(ids)

    async def handle(
        self, amonet_sprint_id: UUID
    ) -> List[ColumnaConTareasDto]:
        columnas, _, _, _ = await self._columna_repository.get_all(
            page=1,
            page_size=999999,
            where=lambda q: q.where(ColumnaKanbanConfiguration.activo == True),
            order_by=ColumnaKanbanConfiguration.posicion.asc(),
        )

        tareas, _, _, _ = await self._tarea_repository.get_all(
            page=1,
            page_size=999999,
            where=lambda q: q.where(
                TareaSprintConfiguration.amonet_sprint_id == amonet_sprint_id,
                TareaSprintConfiguration.activo == True,
            ),
            loader_options=TareaSprintLoaderOptions.get(),
            order_by=TareaSprintConfiguration.fecha_alta.asc(),
        )

        tag_ids = await self._collect_tag_ids(tareas)
        tag_lookup = await TareaSprintMapper.build_tag_lookup(self._session, tag_ids)

        tareas_por_columna: Dict[UUID, list] = {}
        for t in tareas:
            col_id = t.amonet_columna_kanban_id
            if col_id not in tareas_por_columna:
                tareas_por_columna[col_id] = []
            tareas_por_columna[col_id].append(TareaSprintMapper.to_response(t, tag_lookup=tag_lookup))

        resultado = []
        for col in columnas:
            col_id = col.id_amonet_columna_kanban
            resultado.append(ColumnaConTareasDto(
                columna=ColumnaInfoDto(
                    id=col_id,
                    nombre=col.nombre,
                    posicion=col.posicion,
                ),
                tareas=tareas_por_columna.get(col_id, []),
            ))

        return resultado

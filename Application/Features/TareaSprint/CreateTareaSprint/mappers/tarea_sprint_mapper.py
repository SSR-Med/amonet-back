from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from Application.Features.TareaSprint.CreateTareaSprint.dtos import (
    PrioridadInfoDto,
    TagInfoDto,
    TareaSprintResponseDto,
    UsuarioInfoDto,
)
from core.dtos import CurrentUserDto
from infrastructure.dataaccess.configurations import (
    PrioridadKanbanConfiguration,
    TagKanbanConfiguration,
    TareaSprintConfiguration,
)


class TareaSprintMapper:

    @staticmethod
    def _map_usuario(
        rel,
        fallback_id=None,
        current_user: Optional[CurrentUserDto] = None,
    ):
        if rel is not None:
            return UsuarioInfoDto(
                id=rel.id_amonet_usuario,
                documento=rel.documento,
                nombre=rel.nombre,
            )
        if current_user is not None and fallback_id == current_user.id:
            return UsuarioInfoDto(
                id=current_user.id,
                documento=current_user.documento,
                nombre=current_user.nombre,
            )
        if fallback_id is not None:
            return UsuarioInfoDto(id=fallback_id, documento="", nombre="")
        return None

    @staticmethod
    async def build_tag_lookup(
        session: AsyncSession, tag_ids: List[UUID]
    ) -> Dict[UUID, TagInfoDto]:
        if not tag_ids:
            return {}
        result = await session.execute(
            select(TagKanbanConfiguration).where(
                TagKanbanConfiguration.id_amonet_tag_kanban.in_(tag_ids)
            )
        )
        return {
            m.id_amonet_tag_kanban: TagInfoDto(
                id=m.id_amonet_tag_kanban,
                nombre=m.nombre,
                color_red=m.color_red,
                color_green=m.color_green,
                color_blue=m.color_blue,
            )
            for m in result.scalars().all()
        }

    @staticmethod
    async def build_prioridad_lookup(
        session: AsyncSession, prioridad_id: Optional[UUID]
    ) -> Optional[PrioridadInfoDto]:
        if prioridad_id is None:
            return None
        result = await session.execute(
            select(PrioridadKanbanConfiguration).where(
                PrioridadKanbanConfiguration.id_amonet_prioridad_kanban == prioridad_id
            )
        )
        m = result.scalar_one_or_none()
        if m is None:
            return None
        return PrioridadInfoDto(
            id=m.id_amonet_prioridad_kanban,
            nombre=m.nombre,
            color_red=m.color_red,
            color_green=m.color_green,
            color_blue=m.color_blue,
        )

    @staticmethod
    def to_response(
        model: TareaSprintConfiguration,
        current_user: Optional[CurrentUserDto] = None,
        tag_lookup: Optional[Dict[UUID, TagInfoDto]] = None,
        prioridad_lookup: Optional[PrioridadInfoDto] = None,
    ) -> TareaSprintResponseDto:
        tags_dto = []
        if tag_lookup and model.tags:
            for tag_id in model.tags:
                dto = tag_lookup.get(UUID(tag_id) if isinstance(tag_id, str) else tag_id)
                if dto:
                    tags_dto.append(dto)

        prioridad = prioridad_lookup
        if prioridad is None and model.amonet_prioridad_kanban_id:
            prioridad = TareaSprintMapper._map_prioridad_from_model(model)

        return TareaSprintResponseDto(
            id=model.id_amonet_tarea_sprint,
            titulo=model.titulo,
            descripcion=model.descripcion,
            asignado=TareaSprintMapper._map_usuario(
                model.__dict__.get('asignado_rel'),
                model.asignado,
                current_user,
            ),
            fecha_vencimiento=model.fecha_vencimiento,
            tags=tags_dto,
            prioridad=prioridad,
            amonet_sprint_id=model.amonet_sprint_id,
            amonet_columna_kanban_id=model.amonet_columna_kanban_id,
            usuario_alta=TareaSprintMapper._map_usuario(
                model.__dict__.get('usuario_alta_rel'),
                model.usuario_alta,
                current_user,
            ),
            fecha_alta=model.fecha_alta,
            usuario_modifica=TareaSprintMapper._map_usuario(
                model.__dict__.get('usuario_modifica_rel'),
                None,
            ),
            fecha_modifica=model.fecha_modifica,
        )

    @staticmethod
    def _map_prioridad_from_model(model: TareaSprintConfiguration) -> Optional[PrioridadInfoDto]:
        prioridad_rel = model.__dict__.get('prioridad')
        if prioridad_rel is not None:
            return PrioridadInfoDto(
                id=prioridad_rel.id_amonet_prioridad_kanban,
                nombre=prioridad_rel.nombre,
                color_red=prioridad_rel.color_red,
                color_green=prioridad_rel.color_green,
                color_blue=prioridad_rel.color_blue,
            )
        return None


class TareaSprintLoaderOptions:

    @staticmethod
    def get():
        return [
            selectinload(TareaSprintConfiguration.usuario_alta_rel),
            selectinload(TareaSprintConfiguration.usuario_modifica_rel),
            selectinload(TareaSprintConfiguration.asignado_rel),
            selectinload(TareaSprintConfiguration.prioridad),
            selectinload(TareaSprintConfiguration.sprint),
            selectinload(TareaSprintConfiguration.columna),
        ]

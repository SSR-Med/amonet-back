from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.UpdateOrdenProduccionEstado.command import (
    UpdateOrdenProduccionEstadoCommand,
)
from Application.Features.OrdenProduccion.UpdateOrdenProduccionEstado.strategies.base_strategy import (
    BaseStrategy,
)
from infrastructure.dataaccess.configurations import (
    InventarioMateriaPrimaContenedorConfiguration,
    OrdenProduccionConfiguration,
    OrdenProduccionMateriaPrimaConfiguration,
    OrdenProduccionMateriaPrimaContenedorConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class CancelStrategy(BaseStrategy):

    def __init__(self) -> None:
        self._contenedor_orden_repo: Repository = None
        self._inventario_contenedor_repo: Repository = None

    async def execute(
        self,
        order: OrdenProduccionConfiguration,
        command: UpdateOrdenProduccionEstadoCommand,
        session: AsyncSession,
    ) -> None:
        self._contenedor_orden_repo = Repository(
            session, OrdenProduccionMateriaPrimaContenedorConfiguration
        )
        self._inventario_contenedor_repo = Repository(
            session, InventarioMateriaPrimaContenedorConfiguration
        )

        order.amonet_estado_produccion_id = command.amonet_estado_produccion_id
        order.cancel_razon_descripcion = command.cancel_razon_descripcion
        await self._restore_containers(order, session)

    async def _restore_containers(
        self,
        order: OrdenProduccionConfiguration,
        session: AsyncSession,
    ) -> None:
        items, _, _, _ = await self._contenedor_orden_repo.get_all(
            page=1,
            page_size=10000,
            where=lambda q: q.join(
                OrdenProduccionMateriaPrimaConfiguration,
                OrdenProduccionMateriaPrimaContenedorConfiguration.amonet_orden_produccion_materia_prima_id
                == OrdenProduccionMateriaPrimaConfiguration.id_amonet_orden_produccion_materia_prima,
            ).where(
                OrdenProduccionMateriaPrimaConfiguration.amonet_orden_produccion_id
                == order.id_amonet_orden_produccion,
            ),
        )

        for order_cont in items:
            db_contenedor = await self._inventario_contenedor_repo.first_or_default(
                lambda q: q.where(
                    InventarioMateriaPrimaContenedorConfiguration.id_amonet_inventario_materia_prima_contenedor
                    == order_cont.amonet_inventario_materia_prima_contenedor_id
                )
            )
            if db_contenedor:
                db_contenedor.cantidad_disponible += order_cont.cantidad

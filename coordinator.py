"""DataUpdateCoordinator for the Todoist component."""
from datetime import timedelta
import logging

#from todoist_api_python.api_async import TodoistAPIAsync
#from todoist_api_python.models import Label, Project, Task
from icaapi_async import IcaAPIAsync
from icatypes import IcaStore, IcaProductCategory, IcaShoppingListEntry, IcaOffer, IcaShoppingList

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed


class IcaCoordinator(DataUpdateCoordinator[list[IcaShoppingListEntry]]):
    """Coordinator for updating task data from ICA."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        update_interval: timedelta,
        api: IcaAPIAsync
    ) -> None:
        """Initialize the ICA coordinator."""
        super().__init__(hass, logger, name="ICA", update_interval=update_interval)
        self.api = api
        self._stores: list[IcaStore] | None = None
        self._productCategories: list[IcaProductCategory] | None = None
        self._icaOffers: list[IcaOffer] | None = None
        self._icaShoppingLists: list[IcaShoppingList] | None = None        

    async def _async_update_data(self) -> list[IcaShoppingListEntry]:
        """Fetch tasks from the ICA API."""
        try:
            return await self.api.get_tasks()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def async_get_shopping_lists(self) -> list[IcaShoppingList]:
        """Return ICA shopping lists fetched at most once."""
        if self._icaShoppingLists is None:
            self._icaShoppingLists = await self.api.get_shopping_lists()
        return self._icaShoppingLists

    async def async_get_product_categories(self) -> list[IcaProductCategory]:
        """Return ICA product categories fetched at most once."""
        if self._productCategories is None:
            self._productCategories = await self.api.get_product_categories()
        return self._productCategories
   
    async def async_get_stores(self) -> list[IcaStore]:
        """Return ICA favorite stores fetched at most once."""
        if self._stores is None:
            self._stores = await self.api.get_favorite_stores()
        return self._stores

    async def async_get_offers(self) -> list[IcaOffer]:
        """Return ICA offers at favorite stores fetched at most once."""
        stores = self.async_get_stores()
        if self._offers is None:
            self._offers = await self.api.get_offers([s["Id"] for s in stores])
        return self._offers



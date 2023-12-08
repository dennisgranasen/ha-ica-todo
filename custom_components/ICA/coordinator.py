"""DataUpdateCoordinator for the Todoist component."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .icaapi_async import IcaAPIAsync
from .icatypes import (
    IcaStore,
    IcaProductCategory,
    IcaShoppingListEntry,
    IcaOffer,
    IcaShoppingList,
)


class IcaCoordinator(DataUpdateCoordinator[list[IcaShoppingListEntry]]):
    """Coordinator for updating task data from ICA."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        update_interval: timedelta,
        api: IcaAPIAsync,
    ) -> None:
        """Initialize the ICA coordinator."""
        super().__init__(hass, logger, name="ICA", update_interval=update_interval)
        self.api = api
        self._stores: list[IcaStore] | None = None
        self._productCategories: list[IcaProductCategory] | None = None
        self._icaOffers: list[IcaOffer] | None = None
        self._icaShoppingLists: list[IcaShoppingList] | None = None

    def get_shopping_list(self, list_id) -> IcaShoppingList:
        # await self.async_get_shopping_lists()
        for x in filter(lambda x: x["Id"] == list_id, self._icaShoppingLists):
            return x
        return None

    def get_article_group(self, productName) -> int:
        # await self.async_get_product_categories()
        # for x in filter(lambda x: x["Id"] == list_id, self._icaShoppingLists):
        #    return x
        articleGroups = {
            "välling": 9,
            "kaffe": 9,
            "maskindiskmedel": 11,
            "hushållspapper": 11,
            "toapapper": 11,
            "blöjor": 11,
        }

        return articleGroups.get(str.lower(productName), 12)

    async def _async_update_data(self) -> list[IcaShoppingListEntry]:
        """Fetch shopping lists from the ICA API."""
        try:
            # return await self.api.get_tasks()
            lists = await self.async_get_shopping_lists()
            return (
                lists["ShoppingLists"][0]
                if lists and "ShoppingLists" in lists
                else None
            )
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def async_get_shopping_lists(self) -> list[IcaShoppingList]:
        """Return ICA shopping lists fetched at most once."""
        if self._icaShoppingLists is None:
            x = await self.api.get_shopping_lists()
            if "ShoppingLists" in x:
                y = x["ShoppingLists"]
                self._icaShoppingLists = [
                    await self.api.get_shopping_list(z["OfflineId"]) for z in y
                ]

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
        stores = await self.async_get_stores()
        if self._icaOffers is None:
            self._icaOffers = await self.api.get_offers([s["Id"] for s in stores])
        return self._icaOffers

import requests
import asyncio

from icaapi import IcaAPI
from icatypes import IcaShoppingList, IcaStore, IcaOffer, IcaProductCategory


async def run_async(func):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func)


class IcaAPIAsync:
   
    ### Class to retrieve and hold the data for a Shopping list from ICA ###
    def __init__(self, username, password):
        self._api = IcaAPI(username, password)
    
    async def get_shopping_lists(self) -> list[IcaShoppingList]:
        return await run_async(lambda: self._api.get_shopping_lists())
    
    async def get_shopping_list(self, list_id: str) -> IcaShoppingList:
        return await run_async(lambda: self._api.get_shopping_list(list_id))
    
    async def get_store(self, store_id) -> IcaStore:
        return await run_async(lambda: self._api.get_store(store_id))

    async def get_favorite_stores(self) -> [IcaStore]:
        return await run_async(lambda: self._api.get_favorite_stores())
    
    async def get_product_categories(self) -> [IcaProductCategory]:
        return await run_async(lambda: self._api.get_product_categories())
    
    async def get_offers(self, store_ids: list[int]) -> [IcaOffer]:
        return await run_async(lambda: self._api.get_offers(store_ids))
    
    async def create_shopping_list(self, offline_id: int, title: str, comment: str, storeSorting: bool = True):
        return await run_async(lambda: self._api.create_shopping_list(offline_id, title, comment, storeSorting))

    async def sync_shopping_list(self, data: IcaShoppingList):
        return await run_async(lambda: self._api.sync_shopping_list(data))

    async def delete_shopping_list(self, offline_id):
        return await run_async(lambda: self._api.delete_shopping_list(offline_id))

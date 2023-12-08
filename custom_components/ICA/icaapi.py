import requests
from datetime import datetime
from .http_requests import get, post, delete
from .const import (
    AUTH_TICKET,
    LIST_NAME,  
    ITEM_LIST,
    ITEM_NAME,
    IS_CHECKED,
    BASE_URL,
    AUTH_ENDPOINT,
    MY_LIST_ENDPOINT,
    MY_BONUS_ENDPOINT,
    MY_CARDS_ENDPOINT,
    MY_LISTS_ENDPOINT,
    STORE_ENDPOINT,
    OFFERS_ENDPOINT,
    RECIPE_ENDPOINT,
    MY_RECIPES_ENDPOINT,
    MY_STORES_ENDPOINT,
    MY_LIST_SYNC_ENDPOINT,
    STORE_SEARCH_ENDPOINT,
    ARTICLEGROUPS_ENDPOINT,
    RANDOM_RECIPES_ENDPOINT,
    MY_COMMON_ARTICLES_ENDPOINT
)
from icatypes import IcaStore, IcaOffer, IcaShoppingList, IcaProductCategory

def get_rest_url(endpoint: str):
    return '/'.join([BASE_URL, endpoint])

def get_auth_key(user, psw):
    url = get_rest_url(AUTH_ENDPOINT)
    auth = (user, psw)
    response = requests.get(url, auth = auth)
    if response:
        return response.headers[AUTH_TICKET]
    return None


class IcaAPI:
    ### Class to retrieve and manipulate ICA Shopping lists ###
    def __init__(self, user, psw, session: requests.Session | None = None) -> None:
        self._auth_key = get_auth_key(user, psw)
        self._session = session or requests.Session()

    def get_shopping_lists(self) -> list[IcaShoppingList]:
        url = get_rest_url(MY_LISTS_ENDPOINT)
        return get(self._session, url, self._auth_key)        
    
    def get_shopping_list(self, list_id: str) -> IcaShoppingList:
        url = str.format(get_rest_url(MY_LIST_ENDPOINT), list_id)
        return get(self._session, url, self._auth_key)        

    def get_store(self, store_id) -> IcaStore:
        url = str.format(get_rest_url(STORE_ENDPOINT), store_id)
        return get(self._session, url, self._auth_key)

    def get_favorite_stores(self) -> [IcaStore]:
        url = get_rest_url(MY_STORES_ENDPOINT)
        fav_stores = get(self._session, url, self._auth_key)
        return [self.get_store(store_id) for store_id in fav_stores["FavoriteStores"]]
            
    def get_offers(self, store_ids: list[int]) -> [IcaOffer]:
        url = str.format(get_rest_url(OFFERS_ENDPOINT), ','.join(store_ids))
        return get(self._session, url, self._auth_key)
    
    def get_product_categories(self) -> [IcaProductCategory]:
        url = str.format(get_rest_url(ARTICLEGROUPS_ENDPOINT))
        return get(self._session, url, self._auth_key)

    def create_shopping_list(self, offline_id: int, title: str, comment: str, storeSorting: bool = True) -> IcaShoppingList:
        url = get_rest_url(MY_LISTS_ENDPOINT)
        data = {
            "OfflineId": str(offline_id),
            "Title": title,
            "CommentText": comment,
            "SortingStore": 1 if storeSorting else 0,
            "Rows": [],
            "LatestChange": datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        }
        response = post(self._session, url, self._auth_key, data)
        # list_id = response["id"]
        return self.get_shopping_list(offline_id)
    
    def sync_shopping_list(self, data: IcaShoppingList):
        url = str.format(get_rest_url(MY_LIST_SYNC_ENDPOINT), data["OfflineId"])
        return post(self._session, url, self._auth_key, data)

    def delete_shopping_list(self, offline_id: int):
        url = str.format(get_rest_url(MY_LIST_ENDPOINT), offline_id)
        return delete(self._session, url, self._auth_key)
        
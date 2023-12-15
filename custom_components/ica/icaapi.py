import requests
import json
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
    MY_COMMON_ARTICLES_ENDPOINT,
)
from .icatypes import IcaStore, IcaOffer, IcaShoppingList, IcaProductCategory, IcaRecipe


def get_rest_url(endpoint: str):
    return "/".join([BASE_URL, endpoint])


def get_auth_key(user, psw):
    url = get_rest_url(AUTH_ENDPOINT)
    auth = (user, psw)
    response = requests.get(url, auth=auth)
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

    def get_favorite_stores(self) -> list[IcaStore]:
        url = get_rest_url(MY_STORES_ENDPOINT)
        fav_stores = get(self._session, url, self._auth_key)
        return [self.get_store(store_id) for store_id in fav_stores["FavoriteStores"]]

    def get_favorite_products(self):
        url = get_rest_url(MY_COMMON_ARTICLES_ENDPOINT)
        fav_products = get(self._session, url, self._auth_key)
        return (
            fav_products["CommonArticles"] if "CommonArticles" in fav_products else None
        )

    def get_offers(self, store_ids: list[int]) -> list[IcaOffer]:
        url = str.format(
            get_rest_url(OFFERS_ENDPOINT), ",".join(map(lambda x: str(x), store_ids))
        )
        return get(self._session, url, self._auth_key)

    def get_random_recipes(self, nRecipes: int = 5) -> list[IcaRecipe]:
        url = str.format(get_rest_url(RANDOM_RECIPES_ENDPOINT), nRecipes)
        return get(self._session, url, self._auth_key)

    def get_product_categories(self) -> list[IcaProductCategory]:
        url = get_rest_url(
            # str.format(ARTICLEGROUPS_ENDPOINT, datetime.date(datetime.now()))
            str.format(ARTICLEGROUPS_ENDPOINT, "2001-01-01")
        )
        return get(self._session, url, self._auth_key)

    def create_shopping_list(
        self, offline_id: int, title: str, comment: str, storeSorting: bool = True
    ) -> IcaShoppingList:
        url = get_rest_url(MY_LISTS_ENDPOINT)
        data = {
            "OfflineId": str(offline_id),
            "Title": title,
            "CommentText": comment,
            "SortingStore": 1 if storeSorting else 0,
            "Rows": [],
            "LatestChange": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        }
        response = post(self._session, url, self._auth_key, data)
        # list_id = response["id"]
        return self.get_shopping_list(offline_id)

    def sync_shopping_list(self, data: IcaShoppingList):
        url = str.format(get_rest_url(MY_LIST_SYNC_ENDPOINT), data["OfflineId"])
        # new_rows = [x for x in data["Rows"] if "SourceId" in x and x["SourceId"] == -1]
        # data = {"ChangedRows": new_rows}

        if "DeletedRows" in data:
            sync_data = {"DeletedRows": data["DeletedRows"]}
        elif "ChangedRows" in data:
            sync_data = {"ChangedRows": data["ChangedRows"]}
        elif "CreatedRows" in data:
            sync_data = {"CreatedRows": data["CreatedRows"]}
        else:
            sync_data = data

        data2 = post(self._session, url, self._auth_key, sync_data)
        # if data is not None and "Rows" in data:
        #    for row in data["Rows"]:
        #        name = row["ProductName"]
        #        uuid = row["OfflineId"]
        #        status = row["IsStrikedOver"]
        #        source = row["SourceId"]

        return data2

    def delete_shopping_list(self, offline_id: int):
        url = str.format(get_rest_url(MY_LIST_ENDPOINT), offline_id)
        return delete(self._session, url, self._auth_key)

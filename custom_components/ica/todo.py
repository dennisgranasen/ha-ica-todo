"""A todo platform for ICA shopping lists."""

import asyncio
import datetime
from typing import Any, cast

from homeassistant.components.todo import (
    TodoItem,
    TodoItemStatus,
    TodoListEntity,
    TodoListEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import IcaCoordinator
from .icatypes import IcaShoppingList


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the ICA shopping list platform config entry."""
    coordinator: IcaCoordinator = hass.data[DOMAIN][entry.entry_id]
    shopping_lists: list[IcaShoppingList] = await coordinator.async_get_shopping_lists()
    async_add_entities(
        IcaShoppingListEntity(
            coordinator, entry.entry_id, shopping_list["Id"], shopping_list["Title"]
        )
        for shopping_list in shopping_lists
    )


def _task_api_data(item: TodoItem) -> dict[str, Any]:
    """Convert a TodoItem to the set of add or update arguments."""
    item_data: dict[str, Any] = {}
    if summary := item.summary:
        item_data["content"] = summary
    if due := item.due:
        if isinstance(due, datetime.datetime):
            item_data["due"] = {
                "date": due.date().isoformat(),
                "datetime": due.isoformat(),
            }
        else:
            item_data["due"] = {"date": due.isoformat()}
    if description := item.description:
        item_data["description"] = description
    return item_data


class IcaShoppingListEntity(CoordinatorEntity[IcaCoordinator], TodoListEntity):
    """A ICA shopping list TodoListEntity."""

    _attr_supported_features = (
        TodoListEntityFeature.CREATE_TODO_ITEM
        | TodoListEntityFeature.UPDATE_TODO_ITEM
        | TodoListEntityFeature.DELETE_TODO_ITEM
        | TodoListEntityFeature.MOVE_TODO_ITEM
    )

    def __init__(
        self,
        coordinator: IcaCoordinator,
        config_entry_id: str,
        shopping_list_id: str,
        shopping_list_name: str,
    ) -> None:
        """Initialize IcaShoppingListEntity."""
        super().__init__(coordinator=coordinator)
        self._project_id = shopping_list_id
        self._attr_unique_id = f"{config_entry_id}-{shopping_list_id}"
        self._attr_name = shopping_list_name
        self._attr_icon = "icon.png"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        shopping_list = self.coordinator.get_shopping_list(self._project_id)
        items = []
        for task in shopping_list["Rows"]:
            items.append(
                TodoItem(
                    summary=task["ProductName"],
                    uid=task["OfflineId"],
                    status=TodoItemStatus.COMPLETED
                    if task["IsStrikedOver"]
                    else TodoItemStatus.NEEDS_ACTION,
                    description="Beskrivningen...",
                )
            )
        self._attr_todo_items = items
        super()._handle_coordinator_update()

    async def async_create_todo_item(self, item: TodoItem) -> None:
        """Create a To-do item."""
        if item.status != TodoItemStatus.NEEDS_ACTION:
            raise ValueError("Only active tasks may be created.")
        articleGroup = self.coordinator.get_article_group(item.summary)
        shopping_list = self.coordinator.get_shopping_list(self._project_id)

        stuff = {
            "ProductName": item.summary,
            "SourceId": -1,
            "IsStrikedOver": False,
            "ArticleGroupId": articleGroup,
        }
        if "CreatedRows" not in shopping_list:
            shopping_list["CreatedRows"] = []
        shopping_list["CreatedRows"].append(stuff)

        shopping_list["LatestChange"] = (
            datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        )
        await self.coordinator.api.sync_shopping_list(shopping_list)
        await self.coordinator.async_refresh()

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """Update a To-do item."""
        shopping_list = self.coordinator.get_shopping_list(self._project_id)

        if "ChangedRows" not in shopping_list:
            shopping_list["ChangedRows"] = []

        shopping_list["ChangedRows"].append(
            {
                "OfflineId": item.uid,
                "IsStrikedOver": item.status == TodoItemStatus.COMPLETED,
                "SourceId": -1,
            }
        )
        # if item.status is not None:
        #    if item.status == TodoItemStatus.COMPLETED:
        #        await self.coordinator.api.close_task(task_id=uid)
        #    else:
        #        await self.coordinator.api.reopen_task(task_id=uid)

        await self.coordinator.api.sync_shopping_list(shopping_list)
        await self.coordinator.async_refresh()

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        """Delete a To-do item."""
        # await asyncio.gather(
        #     *[self.coordinator.api.remove_from_list(task_id=uid) for uid in uids]
        # )
        shopping_list = self.coordinator.get_shopping_list(self._project_id)

        if "DeletedRows" not in shopping_list:
            shopping_list["DeletedRows"] = []

        # shopping_list["DeletedRows"].extend(list(deleted_ids))
        shopping_list["DeletedRows"].extend(uids)

        await self.coordinator.api.sync_shopping_list(shopping_list)
        await self.coordinator.async_refresh()

    async def async_move_todo_item(self, uid: str, previous_uid: str | None) -> None:
        """Move a To-do item."""
        # await asyncio.gather(
        #     *[self.coordinator.api.remove_from_list(task_id=uid) for uid in uids]
        # )
        shopping_list = self.coordinator.get_shopping_list(self._project_id)
        await self.coordinator.api.sync_shopping_list(shopping_list)
        await self.coordinator.async_refresh()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass update state from existing coordinator data."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()

"""Constants for the Todoist component."""
from typing import Final

CONF_EXTRA_PROJECTS: Final = "custom_projects"
CONF_PROJECT_DUE_DATE: Final = "due_date_days"
CONF_PROJECT_LABEL_WHITELIST: Final = "labels"
CONF_PROJECT_WHITELIST: Final = "include_projects"

# Calendar Platform: Does this calendar event last all day?
ALL_DAY: Final = "all_day"
# Attribute: All tasks in this project
ALL_TASKS: Final = "all_tasks"
# Todoist API: "Completed" flag -- 1 if complete, else 0
CHECKED: Final = "checked"
# Attribute: Is this task complete?
COMPLETED: Final = "completed"
# Todoist API: What is this task about?
# Service Call: What is this task about?
CONTENT: Final = "content"
# Calendar Platform: Get a calendar event's description
DESCRIPTION: Final = "description"
# Calendar Platform: Used in the '_get_date()' method
DATETIME: Final = "dateTime"
DUE: Final = "due"
# Service Call: When is this task due (in natural language)?
DUE_DATE_STRING: Final = "due_date_string"
# Service Call: The language of DUE_DATE_STRING
DUE_DATE_LANG: Final = "due_date_lang"
# Service Call: When should user be reminded of this task (in natural language)?
REMINDER_DATE_STRING: Final = "reminder_date_string"
# Service Call: The language of REMINDER_DATE_STRING
REMINDER_DATE_LANG: Final = "reminder_date_lang"
# Service Call: The available options of DUE_DATE_LANG
DUE_DATE_VALID_LANGS: Final = [
    "en",
    "sv"
]
# Attribute: When is this task due?
# Service Call: When is this task due?
DUE_DATE: Final = "due_date"
# Service Call: When should user be reminded of this task?
REMINDER_DATE: Final = "reminder_date"
# Attribute: Is this task due today?
DUE_TODAY: Final = "due_today"
# Calendar Platform: When a calendar event ends
END: Final = "end"
# Todoist API: Look up a Project/Label/Task ID
ID: Final = "id"
# Todoist API: Fetch all labels
# Service Call: What are the labels attached to this task?
LABELS: Final = "labels"
# Todoist API: "Name" value
NAME: Final = "name"
# Todoist API: "Full Name" value
FULL_NAME: Final = "full_name"
# Attribute: Is this task overdue?
OVERDUE: Final = "overdue"
# Attribute: What is this task's priority?
# Todoist API: Get a task's priority
# Service Call: What is this task's priority?
PRIORITY: Final = "priority"
# Todoist API: Look up the Project ID a Task belongs to
PROJECT_ID: Final = "project_id"
# Service Call: What Project do you want a Task added to?
PROJECT_NAME: Final = "project"
# Todoist API: Fetch all Projects
PROJECTS: Final = "projects"
# Calendar Platform: When does a calendar event start?
START: Final = "start"
# Calendar Platform: What is the next calendar event about?
SUMMARY: Final = "summary"
# Todoist API: Fetch all Tasks
TASKS: Final = "items"
# Todoist API: "responsible" for a Task
ASSIGNEE: Final = "assignee"
# Todoist API: Collaborators in shared projects
COLLABORATORS: Final = "collaborators"

SERVICE_NEW_TASK: Final = "new_task"


"""Constants for ICA shopping list"""

DOMAIN: Final = "icashopping"
CONF_USERNAME: Final = "personal id"
CONF_PASSWORD: Final = "pin code"
AUTH_TICKET: Final = "AuthenticationTicket"
GET_LISTS: Final = "ShoppingLists"
LIST_NAME: Final = "Title"
ITEM_LIST: Final = "Rows"
ITEM_NAME: Final = "ProductName"
IS_CHECKED: Final = "IsStrikedOver"

BASE_URL: Final = "https://handla.api.ica.se/api/"

AUTH_ENDPOINT: Final = "login"
MY_LISTS_ENDPOINT: Final = "user/offlineshoppinglists"
MY_LIST_ENDPOINT: Final = "user/offlineshoppinglists/{}"
MY_LIST_SYNC_ENDPOINT: Final = "user/offlineshoppinglists/{}/sync"
MY_CARDS_ENDPOINT: Final = "user/cardaccounts"
MY_BONUS_ENDPOINT: Final = "user/minbonustransaction"
MY_STORES_ENDPOINT: Final = "user/stores"
MY_RECIPES_ENDPOINT: Final = "user/recipes"
MY_COMMON_ARTICLES_ENDPOINT: Final = "user/commonarticles/{}{}"
STORE_ENDPOINT: Final = "stores/{}"
STORE_SEARCH_ENDPOINT: Final = "stores/search?Filters&Phrase={}"
OFFERS_ENDPOINT: Final = "offers?Stores={}"
ARTICLEGROUPS_ENDPOINT: Final = "articles/articlegroups?lastsyncdate={}"
RECIPE_ENDPOINT: Final = "recipe"
RANDOM_RECIPES_ENDPOINT: Final = "recipes/random?numberofrecipes={}"
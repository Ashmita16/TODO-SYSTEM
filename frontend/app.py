import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

def format_date(date_string):

    if not date_string:
        return "N/A"

    try:
        date = datetime.fromisoformat(
            date_string.replace("Z", "")
        )

        return date.strftime(
            "%d %B %Y, %I:%M %p"
        )

    except Exception:
        return date_string


def get_error(response):

    try:
        data = response.json()

        if isinstance(data, dict):
            return data.get(
                "detail",
                "Something went wrong"
            )

        return "Something went wrong"

    except Exception:
        return (
            f"Server returned status "
            f"{response.status_code}"
        )


def display_category(category):

    st.subheader("Category Details")

    st.write(
        "**ID:**",
        category["id"]
    )

    st.write(
        "**Name:**",
        category["name"]
    )

    st.write(
        "**Description:**",
        category["description"]
    )

    st.write(
        "**Created At:**",
        format_date(
            category["created_at"]
        )
    )

    st.write(
        "**Updated At:**",
        format_date(
            category["updated_at"]
        )
    )


def display_todo(todo):

    st.subheader("Todo Details")

    st.write(
        "**ID:**",
        todo["id"]
    )

    st.write(
        "**Title:**",
        todo["title"]
    )

    st.write(
        "**Description:**",
        todo["description"]
    )

    st.write(
        "**Completed:**",
        todo["is_completed"]
    )

    st.write(
        "**Status:**",
        todo["status"]
    )

    st.write(
        "**Priority:**",
        todo["priority"]
    )

    st.write(
        "**Category ID:**",
        todo["category_id"]
    )

    st.write(
        "**Estimated Hours:**",
        todo["estimated_hours"]
    )

    st.write(
        "**Due Date:**",
        format_date(
            todo["due_date"]
        )
    )

    st.write(
        "**Created At:**",
        format_date(
            todo["created_at"]
        )
    )

    st.write(
        "**Updated At:**",
        format_date(
            todo["updated_at"]
        )
    )


def prepare_todos(todos):

    formatted_todos = []

    for todo in todos:

        todo_copy = todo.copy()

        todo_copy["created_at"] = format_date(
            todo_copy["created_at"]
        )

        todo_copy["updated_at"] = format_date(
            todo_copy["updated_at"]
        )

        todo_copy["due_date"] = format_date(
            todo_copy["due_date"]
        )

        formatted_todos.append(
            todo_copy
        )

    return formatted_todos

st.set_page_config(
    page_title="TODO MANAGEMENT SYSTEM",
    layout="wide"
)


st.sidebar.title(
    "TODO MANAGEMENT SYSTEM"
)

option = st.sidebar.selectbox(
    "Select Operation",
    [
        "Home",
        "Create Category",
        "View Categories",
        "Get Category by ID",
        "Update Category",
        "Delete Category",
        "Create Todo",
        "View All Todos",
        "Get Todo by ID",
        "Get Todos by Category",
        "Search & Filter Todos",
        "Update Todo",
        "Delete Todo",
        "Delete All Todos by Category"
    ]
)

if option == "Home":

    st.title(
        "TODO MANAGEMENT SYSTEM"
    )

    st.subheader(
        "API STATUS"
    )

    if st.button(
        "CHECK API STATUS"
    ):

        try:

            response = requests.get(
                API_URL + "/",
                timeout=5
            )

            if response.status_code == 200:

                st.success(
                    "FASTAPI IS RUNNING"
                )

                st.json(
                    response.json()
                )

            else:

                st.error(
                    get_error(response)
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FASTAPI IS NOT RUNNING"
            )

        except requests.exceptions.Timeout:

            st.error(
                "The API request timed out"
            )


elif option == "Create Category":

    st.title(
        "CREATE CATEGORY"
    )

    name = st.text_input(
        "CATEGORY NAME"
    )

    description = st.text_area(
        "DESCRIPTION"
    )

    if st.button(
        "CREATE CATEGORY"
    ):

        if not name.strip():

            st.warning(
                "Please enter category name"
            )

        elif not description.strip():

            st.warning(
                "Please enter description"
            )

        else:

            data = {
                "name": name.strip(),
                "description": description.strip()
            }

            try:

                response = requests.post(
                    API_URL + "/categories",
                    json=data,
                    timeout=5
                )

                if response.status_code == 201:

                    st.success(
                        "Category created successfully"
                    )

                    category = response.json()

                    display_category(
                        category
                    )

                else:

                    st.error(
                        get_error(response)
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI is not running"
                )

elif option == "View Categories":

    st.title(
        "VIEW ALL CATEGORIES"
    )

    if st.button(
        "LOAD CATEGORIES"
    ):

        try:

            response = requests.get(
                API_URL + "/categories",
                timeout=5
            )

            if response.status_code == 200:

                categories = response.json()

                if categories:

                    formatted_categories = []

                    for category in categories:

                        category_copy = category.copy()

                        category_copy["created_at"] = format_date(
                            category_copy["created_at"]
                        )

                        category_copy["updated_at"] = format_date(
                            category_copy["updated_at"]
                        )

                        formatted_categories.append(
                            category_copy
                        )

                    st.dataframe(
                        formatted_categories,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "NO CATEGORIES FOUND"
                    )

            else:

                st.error(
                    get_error(response)
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI is not running"
            )

elif option == "Get Category by ID":

    st.title(
        "GET CATEGORY BY ID"
    )

    category_id = st.number_input(
        "CATEGORY ID",
        min_value=1,
        step=1
    )

    if st.button(
        "GET CATEGORY"
    ):

        try:

            response = requests.get(
                API_URL + f"/categories/{category_id}",
                timeout=5
            )

            if response.status_code == 200:

                st.success(
                    "CATEGORY FOUND"
                )

                category = response.json()

                display_category(
                    category
                )

            else:

                st.error(
                    get_error(response)
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI is not running"
            )


elif option == "Update Category":

    st.title(
        "UPDATE CATEGORY"
    )

    category_id = st.number_input(
        "CATEGORY ID",
        min_value=1,
        step=1
    )

    name = st.text_input(
        "NEW NAME"
    )

    description = st.text_area(
        "NEW DESCRIPTION"
    )

    if st.button(
        "UPDATE CATEGORY"
    ):

        data = {}

        if name.strip():

            data["name"] = name.strip()

        if description.strip():

            data["description"] = description.strip()

        if not data:

            st.warning(
                "Enter at least one field to update"
            )

        else:

            try:

                response = requests.put(
                    API_URL + f"/categories/{category_id}",
                    json=data,
                    timeout=5
                )

                if response.status_code == 200:

                    st.success(
                        "Category updated successfully"
                    )

                    category = response.json()

                    display_category(
                        category
                    )

                else:

                    st.error(
                        get_error(response)
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI is not running"
                )

elif option == "Delete Category":

    st.title(
        "DELETE CATEGORY"
    )

    category_id = st.number_input(
        "CATEGORY ID",
        min_value=1,
        step=1
    )

    cascade = st.checkbox(
        "Also delete all Todos belonging to this Category"
    )

    if st.button(
        "DELETE CATEGORY"
    ):

        try:

            response = requests.delete(
                API_URL + f"/categories/{category_id}",
                params={
                    "cascade_delete": cascade
                },
                timeout=5
            )

            if response.status_code == 200:

                st.success(
                    "Category deleted successfully"
                )

                st.json(
                    response.json()
                )

            else:

                st.error(
                    get_error(response)
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI is not running"
            )

elif option == "Create Todo":

    st.title(
        "CREATE TODO"
    )

    title = st.text_input(
        "TODO TITLE"
    )

    description = st.text_area(
        "TODO DESCRIPTION"
    )

    is_completed = st.checkbox(
        "COMPLETED"
    )

    status_value = st.selectbox(
        "STATUS",
        [
            "pending",
            "in_progress",
            "completed",
            "archived"
        ]
    )

    priority = st.selectbox(
        "PRIORITY",
        [
            "low",
            "medium",
            "high",
            "critical"
        ]
    )

    due_date = st.text_input(
        "DUE DATE",
        placeholder="2026-09-20T18:00:00"
    )

    estimated_hours = st.number_input(
        "ESTIMATED HOURS",
        min_value=0.0,
        step=0.5
    )

    category_id = st.number_input(
        "CATEGORY ID",
        min_value=1,
        step=1
    )

    if st.button(
        "CREATE TODO"
    ):

        if not title.strip():

            st.warning(
                "Please enter a Todo title."
            )

        elif not description.strip():

            st.warning(
                "Please enter Todo description."
            )

        else:

            data = {
                "title": title.strip(),
                "description": description.strip(),
                "is_completed": is_completed,
                "status": status_value,
                "priority": priority,
                "due_date": (
                    due_date.strip()
                    if due_date.strip()
                    else None
                ),
                "estimated_hours": estimated_hours,
                "category_id": category_id
            }

            try:

                response = requests.post(
                    API_URL + "/todos",
                    json=data,
                    timeout=5
                )

                if response.status_code == 201:

                    st.success(
                        "Todo created successfully"
                    )

                    todo = response.json()

                    display_todo(
                        todo
                    )

                else:

                    st.error(
                        get_error(response)
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI is not running"
                )

elif option == "View All Todos":

    st.title(
        "VIEW ALL TODOS"
    )

    if st.button(
        "LOAD ALL TODOS"
    ):

        try:

            response = requests.get(
                API_URL + "/todos",
                timeout=5
            )

            if response.status_code == 200:

                todos = response.json()

                if todos:

                    formatted_todos = prepare_todos(
                        todos
                    )

                    st.dataframe(
                        formatted_todos,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No Todos found"
                    )

            else:

                st.error(
                    get_error(response)
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI is not running"
            )

elif option == "Get Todo by ID":

    st.title(
        "GET TODO BY ID"
    )

    todo_id = st.text_input(
        "TODO ID"
    )

    if st.button(
        "GET TODO"
    ):

        if not todo_id:

            st.warning(
                "Please enter Todo ID"
            )

        else:

            try:

                response = requests.get(
                    API_URL + f"/todos/{todo_id}",
                    timeout=5
                )

                if response.status_code == 200:

                    st.success(
                        "Todo found!"
                    )

                    todo = response.json()

                    display_todo(
                        todo
                    )

                else:

                    st.error(
                        get_error(response)
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI is not running"
                )

elif option == "Get Todos by Category":

    st.title(
        "GET TODOS BY CATEGORY"
    )

    category_id = st.number_input(
        "CATEGORY ID",
        min_value=1,
        step=1
    )

    if st.button(
        "GET TODOS"
    ):

        try:

            response = requests.get(
                API_URL + f"/todos/category/{category_id}",
                timeout=5
            )

            if response.status_code == 200:

                todos = response.json()

                if todos:

                    formatted_todos = prepare_todos(
                        todos
                    )

                    st.dataframe(
                        formatted_todos,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No Todos found for this Category"
                    )

            else:

                st.error(
                    get_error(response)
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI is not running"
            )

elif option == "Search & Filter Todos":

    st.title(
        "SEARCH AND FILTER TODOS"
    )

    search = st.text_input(
        "SEARCH BY TITLE OR DESCRIPTION"
    )

    completion = st.selectbox(
        "COMPLETION STATUS",
        [
            "All",
            "Completed",
            "Not Completed"
        ]
    )

    priority = st.selectbox(
        "PRIORITY",
        [
            "All",
            "low",
            "medium",
            "high",
            "critical"
        ]
    )

    status_value = st.selectbox(
        "STATUS",
        [
            "All",
            "pending",
            "in_progress",
            "completed",
            "archived"
        ]
    )

    category_id = st.number_input(
        "CATEGORY ID (0 = All)",
        min_value=0,
        step=1
    )

    st.subheader(
        "PAGINATION"
    )

    skip = st.number_input(
        "SKIP",
        min_value=0,
        value=0,
        step=1
    )

    limit = st.number_input(
        "LIMIT",
        min_value=1,
        max_value=100,
        value=10,
        step=1
    )

    if st.button(
        "SEARCH/FILTER"
    ):

        params = {
            "skip": skip,
            "limit": limit
        }

        if search.strip():

            params["search"] = search.strip()

        if completion == "Completed":

            params["is_completed"] = True

        elif completion == "Not Completed":

            params["is_completed"] = False

        if priority != "All":

            params["priority"] = priority

        if status_value != "All":

            params["status"] = status_value

        if category_id != 0:

            params["category_id"] = category_id

        try:

            response = requests.get(
                API_URL + "/todos",
                params=params,
                timeout=5
            )

            if response.status_code == 200:

                todos = response.json()

                if todos:

                    formatted_todos = prepare_todos(
                        todos
                    )

                    st.dataframe(
                        formatted_todos,
                        use_container_width=True
                    )

                    st.success(
                        f"{len(todos)} Todo(s) found"
                    )

                else:

                    st.info(
                        "No matching Todos found"
                    )

            else:

                st.error(
                    get_error(response)
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI is not running"
            )


elif option == "Update Todo":

    st.title(
        "UPDATE TODO"
    )

    todo_id = st.text_input(
        "TODO ID"
    )

    st.write(
        "ENTER THE FIELDS YOU WANT TO UPDATE"
    )

    title = st.text_input(
        "NEW TITLE"
    )

    description = st.text_area(
        "NEW DESCRIPTION"
    )

    is_completed = st.selectbox(
        "COMPLETION",
        [
            "Do not change",
            "Completed",
            "Not Completed"
        ]
    )

    status_value = st.selectbox(
        "NEW STATUS",
        [
            "Do not change",
            "pending",
            "in_progress",
            "completed",
            "archived"
        ]
    )

    priority = st.selectbox(
        "NEW PRIORITY",
        [
            "Do not change",
            "low",
            "medium",
            "high",
            "critical"
        ]
    )

    due_date = st.text_input(
        "NEW DUE DATE",
        placeholder="2026-09-20T18:00:00"
    )

    estimated_hours = st.number_input(
        "NEW ESTIMATED HOURS (-1 = DO NOT CHANGE)",
        min_value=-1.0,
        value=-1.0,
        step=0.5
    )

    category_id = st.number_input(
        "NEW CATEGORY ID (0 = DO NOT CHANGE)",
        min_value=0,
        step=1
    )

    if st.button(
        "UPDATE TODO"
    ):

        if not todo_id:

            st.warning(
                "Please enter Todo ID."
            )

        else:

            data = {}

            if title.strip():

                data["title"] = title.strip()

            if description.strip():

                data["description"] = description.strip()

            if is_completed == "Completed":

                data["is_completed"] = True

            elif is_completed == "Not Completed":

                data["is_completed"] = False

            if status_value != "Do not change":

                data["status"] = status_value

            if priority != "Do not change":

                data["priority"] = priority

            if due_date.strip():

                data["due_date"] = due_date.strip()

            if estimated_hours >= 0:

                data["estimated_hours"] = estimated_hours

            if category_id != 0:

                data["category_id"] = category_id

            if not data:

                st.warning(
                    "Please enter at least one field to update"
                )

            else:

                try:

                    response = requests.put(
                        API_URL + f"/todos/{todo_id}",
                        json=data,
                        timeout=5
                    )

                    if response.status_code == 200:

                        st.success(
                            "Todo updated successfully!"
                        )

                        todo = response.json()

                        display_todo(
                            todo
                        )

                    else:

                        st.error(
                            get_error(response)
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "FastAPI is not running"
                    )

elif option == "Delete Todo":

    st.title(
        "DELETE TODO"
    )

    todo_id = st.text_input(
        "TODO ID"
    )

    if st.button(
        "DELETE TODO"
    ):

        if not todo_id:

            st.warning(
                "Please enter Todo ID"
            )

        else:

            try:

                response = requests.delete(
                    API_URL + f"/todos/{todo_id}",
                    timeout=5
                )

                if response.status_code == 200:

                    st.success(
                        "Todo deleted successfully"
                    )

                    st.json(
                        response.json()
                    )

                else:

                    st.error(
                        get_error(response)
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI is not running"
                )

elif option == "Delete All Todos by Category":

    st.title(
        "DELETE ALL TODOS BY CATEGORY"
    )

    category_id = st.number_input(
        "CATEGORY ID",
        min_value=1,
        step=1
    )

    if st.button(
        "DELETE ALL TODOS"
    ):

        try:

            response = requests.delete(
                API_URL + f"/todos/category/{category_id}",
                timeout=5
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "Todos deleted successfully"
                )

                st.write(
                    "Deleted count:",
                    result.get(
                        "deleted_count",
                        0
                    )
                )

            else:

                st.error(
                    get_error(response)
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI is not running"
            )


# ---------------------------------------------------------
# MENU MANAGEMENT API
# ---------------------------------------------------------
# This application retrieves restaurant menu items stored
# in an in-memory Python list.
# No database is involved.
# Users can retrieve all menu items, filter items by category
# and availability, and fetch individual items by ID.
# ---------------------------------------------------------


# Import FastAPI to create the application
# Query is used to define and validate query parameters
# HTTPException is used to return custom HTTP error responses
from fastapi import FastAPI, Query, HTTPException

# Uvicorn is the ASGI server used to run our FastAPI application
import uvicorn

# Import Pydantic models used for request/response validation
from model import MenuResponse, MenuItem

# Import the in-memory menu data
from menu import menu_items


# ---------------------------------------------------------
# FASTAPI APPLICATION CONFIGURATION
# ---------------------------------------------------------

app = FastAPI(
    title="Menu APP API's",
    # Title displayed in the API documentation (Swagger UI)

    description="This app retrieves restaurant menu items stored in memory without using a database.",
    # Description displayed in the API documentation

    docs_url="/docs",
    # URL path for Swagger UI documentation

    redoc_url="/redoc",
    # URL path for ReDoc documentation

    openapi_url="/openapi.json"
    # URL path for the OpenAPI JSON specification
)


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------

@app.get("/")
def root():
    # Health-check endpoint to verify whether the API is running

    return {
        "message": "endpoint healthy",
        "status": "healthy"
    }


# ---------------------------------------------------------
# GET ALL MENU ITEMS / FILTER MENU ITEMS
# ---------------------------------------------------------

@app.get("/menu", response_model=MenuResponse)
def get_menu(

    # Optional query parameter to filter menu items by category
    # Example: /menu?category=snacks
    # Default value is None, meaning no category filter is applied

    category: str | None = Query(
        None,
        description="Filter by category"
    ),

    # Optional Boolean query parameter to filter by availability
    # Default value is True, so only available items are returned
    #
    # True  -> Return available items
    # False -> Return unavailable items
    # None  -> Return both available and unavailable items

    available: bool | None = Query(
        True,
        description="Filter by availability. Defaults to available items only."
    )
):

    # Initially assign all menu items to the filtered list
    filtered = menu_items

    # -----------------------------------------------------
    # CATEGORY FILTERING
    # -----------------------------------------------------

    # Check whether the user has provided a category
    if category is not None:

        # Filter menu items based on the requested category
        # category.lower() converts the input to lowercase
        # to make the comparison case-insensitive for input

        filtered = [
            item for item in filtered
            if item["category"] == category.lower()
        ]

    # -----------------------------------------------------
    # AVAILABILITY FILTERING
    # -----------------------------------------------------

    # Check whether the user has provided an availability value
    # If None, skip availability filtering

    if available is not None:

        # Filter menu items based on their availability status
        # Only items matching the requested Boolean value are retained

        filtered = [
            item for item in filtered
            if item["available"] == available
        ]

    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------

    # Check whether any menu items match the applied filters
    # If the filtered list is empty, return HTTP 404 Not Found

    if not filtered:
        raise HTTPException(
            status_code=404,
            detail="No matching menu items found"
        )

    # -----------------------------------------------------
    # API RESPONSE
    # -----------------------------------------------------

    # Return the total number of matching items and the items themselves
    # MenuResponse validates the structure of the returned response

    return MenuResponse(
        count=len(filtered),
        items=filtered
    )


# ---------------------------------------------------------
# GET A SINGLE MENU ITEM USING ITS ID
# ---------------------------------------------------------

@app.get("/menu/{item_id}", response_model=MenuItem)
def get_item(item_id: int):

    # Iterate through the in-memory menu list
    for item in menu_items:

        # Compare the requested ID with the ID of each menu item
        if item["id"] == item_id:

            # Return the matching menu item
            # FastAPI validates the response using MenuItem model
            return item

    # If no matching item is found, return HTTP 404 Not Found
    raise HTTPException(
        status_code=404,
        detail=f"No item found for item_id {item_id}"
    )


# ---------------------------------------------------------
# PROGRAMMATIC UVICORN STARTUP
# ---------------------------------------------------------

if __name__ == "__main__":

    # Start the FastAPI application using Uvicorn
    uvicorn.run(
        "main:app",
        # main -> Python file name (main.py)
        # app  -> FastAPI application instance

        host="127.0.0.1",
        # Run the application on localhost

        port=8001,
        # Port number on which the API server listens

        reload=True
        # Automatically restart the server whenever code changes
        # Recommended for development, not production
    )
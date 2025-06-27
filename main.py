from fastapi import FastAPI
from pydantic import BaseModel
from test import greet

# Initialize the FastAPI app
app = FastAPI()

# --- Define a Pydantic model for request body (optional, but good practice for POST/PUT) ---
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# --- Root endpoint ---
@app.get("/")
async def read_root():
    """
    Returns a simple welcome message.
    """
    return {"message": "Hello, FastAPI!"}

# --- Endpoint with a path parameter ---
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    """
    Retrieves an item by its ID.
    Optionally accepts a query parameter 'q'.
    """
    if q:
        return {"item_id": item_id, "q": q, "message": f"You searched for item {item_id} with query '{q}'"}
    return {"item_id": item_id, "message": f"This is item {item_id}"}

# --- Endpoint with a POST request body ---
@app.post("/items/")
async def create_item(item: Item):
    """
    Creates a new item using a Pydantic model for the request body.
    """
    item_dict = item.model_dump() # Convert Pydantic model to a dictionary
    if item.tax:
        price_with_tax = item.price * (1 + item.tax)
        item_dict.update({"price_with_tax": price_with_tax})
    return {"message": "Item created successfully!", "item": item_dict}

# --- Example of a simple GET endpoint with a query parameter ---
@app.get("/greet/")
async def greet_name(name: str = "Guest"):
    """
    Greets a user by name. Defaults to "Guest" if no name is provided.
    """
    return {"message": f"Hello, {name}!"}

@app.get("/greet/")
async def greet_name_2(name: str = "Guest"):
    """
    Greets a user by name. Defaults to "Guest" if no name is provided.
    """
    return {"message": greet(name)}

# --- How to run this application ---
# 1. Save the code: Save this code as a Python file (e.g., `main.py`).
# 2. Install dependencies:
#    pip install fastapi uvicorn
# 3. Run the application:
#    uvicorn main:app --reload
#
# Once running, you can access the API at:
# - http://127.0.0.1:8000/
# - http://127.0.0.1:8000/items/123
# - http://127.0.0.1:8000/items/123?q=somequery
# - http://127.0.0.1:8000/greet/
# - http://127.0.0.1:8000/greet/?name=Alice
#
# You can test the POST endpoint using tools like Postman, Insomnia, or curl:
# curl -X POST -H "Content-Type: application/json" -d '{"name": "Book", "description": "A great novel", "price": 19.99, "tax": 0.05}' http://127.0.0.1:8000/items/
#
# FastAPI also automatically generates interactive API documentation (Swagger UI) at:
# - http://127.0.0.1:8000/docs
# - Or ReDoc at: http://127.0.0.1:8000/redoc
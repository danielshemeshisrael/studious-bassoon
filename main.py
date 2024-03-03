from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for request body validation
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

# Sample data to mimic database
fake_items_db = [{"name": "item1", "price": 100.0, "is_offer": False}, 
                 {"name": "item2", "price": 200.0, "is_offer": True}]

# Route to get a specific item by its name
@app.get("/items/{item_name}")
async def read_item(item_name: str):
    for item in fake_items_db:
        if item["name"] == item_name:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Route to create a new item
@app.post("/items/")
async def create_item(item: Item):
    fake_items_db.append(item.dict())
    return {"message": "Item created successfully", "item": item}

# Route to update an existing item
@app.put("/items/{item_name}")
async def update_item(item_name: str, item: Item):
    for stored_item in fake_items_db:
        if stored_item["name"] == item_name:
            stored_item.update(item.dict())
            return {"message": "Item updated successfully", "item": stored_item}
    raise HTTPException(status_code=404, detail="Item not found")

# Route to delete an item
@app.delete("/items/{item_name}")
async def delete_item(item_name: str):
    for index, stored_item in enumerate(fake_items_db):
        if stored_item["name"] == item_name:
            del fake_items_db[index]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

from fastapi import FastAPI

# Create an instance of the FastAPI class, TODO: CHECK PARAMETERS
app = FastAPI(
    title="My Simple API",
    description="This is a fantastic starting point for a Python API.",
    version="1.0.0",
)

@app.get("/")
async def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Hello, World! Your API is up and running."}

@app.get("/items/{item_id}")
async def read_item(item_id: int, query_param: str | None = None):
    """
    An endpoint with a path parameter and an optional query parameter.
    """
    response = {"item_id": item_id}
    if query_param:
        response["query_param"] = query_param
    return response

# To run this app, you would use an ASGI server like Uvicorn:
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload   , TODO:DO NOT LEFT THIS BEHIND

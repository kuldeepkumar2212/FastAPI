from fastapi import FastAPI
from fastapi import  requests
import uvicorn

from fastapi import FastAPI

app = FastAPI(
    # API title displayed in the Swagger UI documentation
    title="Basic FastAPI",

    # Description of what the API does.
    # This appears below the title in the API documentation.
    description="Building this FastAPI for learning and experimenting with FastAPI.",

    # Version of your API.
    # This is your API version, not the FastAPI framework version.
    version="1.0.0.0",

    # URL path for Swagger UI documentation.
    # Swagger UI allows us to interactively test API endpoints.
    docs_url="/docs",

    # URL path for ReDoc documentation.
    # ReDoc provides an alternative, read-friendly API documentation interface.
    redoc_url="/redoc",

    # URL path for the OpenAPI JSON schema.
    # This contains the API specification, including endpoints,
    # request parameters, response schemas and other API details.
    openapi_url="/openapi.json"

)

@app.get("/")
def hello():
    """hello route endpoint - health check route"""
    # fast api automatically converts the below dictonary to json and returns as the result. 
    return {"message":"hello get route","status":"healthy"}

    #to run this app we can use uvicorn. 
    # uvicorn main:app --reload --port 8080 
    # main - file name
    # app - the application name where the fast api is initiallized
    # --reload --port are the options, --reload to automatically reload the web server if any changes made to the file --port to specify the port where the app should run
    
# Programmatic Uvicorn Startup
if __name__ == "__main__":

    uvicorn.run(
        "main:app",       # Python file name : FastAPI instance name
        host="127.0.0.1", # Host IP address (localhost)
        port=8080,        # Port on which the server runs
        reload=True       # Automatically restart when code changes
    )
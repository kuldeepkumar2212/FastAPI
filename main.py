from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def hello():
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
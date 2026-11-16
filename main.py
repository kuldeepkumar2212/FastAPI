from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message":"hello from get route","status":"healthy"}

    #to run this app we can use uvicorn. 
    # uvicorn main:app --reload --port 8080 
    # main - file name
    # app - the application name where the fast api is initiallized
    # --reload --port are the options, --reload to automatically reload the web server if any changes made to the file --port to specify the port where the app should run
    
    

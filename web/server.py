from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/", status_code=404)
def rootNotFound():
    print("get / api")
    return {"message": "Resource Not Found"}

@app.get("/main", status_code=404)
def mainNotFound():
    print("get /main api")
    return {"message": "Resource Not Found"}

@app.get("/login", status_code=404)
def loginNotFound():
    print("get /login api")
    return {"message": "Resource Not Found"}

@app.get("/admin", status_code=404)
def adminNotFound():
    print("get /admin api")
    return {"message": "Resource Not Found"}

uvicorn.run(app, host='0.0.0.0', port=8000)
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/", status_code=404)
def rootNotFound():
    print("INFO WEB get / api")
    return {"message": "Resource Not Found"}

@app.get("/main", status_code=404)
def mainNotFound():
    print("INFO WEB get /main api")
    return {"message": "Resource Not Found"}

@app.get("/login", status_code=404)
def loginNotFound():
    print("INFO WEB get /login api")
    return {"message": "Resource Not Found"}

@app.get("/admin", status_code=404)
def adminNotFound():
    print("INFO WEB get /admin api")
    return {"message": "Resource Not Found"}

uvicorn.run(app, host='0.0.0.0', port=8000)

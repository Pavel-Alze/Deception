from fastapi import FastAPI, status
import uvicorn
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def rootNotFound():
    print("INFO WEB get / api")
    return FileResponse("main.html", status_code=status.HTTP_404_NOT_FOUND)

@app.get("/main")
def mainNotFound():
    print("INFO WEB get /main api")
    return FileResponse("main.html", status_code=status.HTTP_404_NOT_FOUND)

@app.get("/login")
def loginNotFound():
    print("INFO WEB get /login api")
    return FileResponse("main.html", status_code=status.HTTP_404_NOT_FOUND)

@app.get("/admin")
def adminNotFound():
    print("INFO WEB get /admin api")
    return FileResponse("main.html", status_code=status.HTTP_404_NOT_FOUND)

uvicorn.run(app, host='0.0.0.0', port=8000)

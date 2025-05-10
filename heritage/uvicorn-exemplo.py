from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
@app.get('/')

async def home() -> JSONResponse:
    return JSONResponse(content={"message":"o mamae e papai!"})
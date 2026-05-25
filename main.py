import uvicorn
from fastapi import FastAPI

from src.url_shortner.api.routes import router
from src.url_shortner.lifespan import lifespan

app = FastAPI(title="url-shortener", lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

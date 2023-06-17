import uvicorn

from blog import app
from fastapi.responses import RedirectResponse
from settings import Config
from blog.routes import router


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")

app.include_router(router)

uvicorn.run(
    "blog:app",
    host=Config.app_host,
    port=Config.app_port,

)

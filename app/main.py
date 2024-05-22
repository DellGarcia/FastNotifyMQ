from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse, JSONResponse

from app.config.log_config import setup_logging
from app.controllers.user_controller import user_router

logger = setup_logging()
logger.info('Starting application')

app = FastAPI()
app.include_router(user_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred"}
    )


@app.get("/", tags=["Redirect"], include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/docs", tags=["Redirect"], include_in_schema=False)
async def get_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Swagger UI"
    )


@app.get("/openapi.json", tags=["Redirect"], include_in_schema=False)
async def get_openapi():
    return get_swagger_ui(
        title="Users API",
        version="1.0.0",
        description="API para gerenciamento de usuários",
        routes=app.routes,
    )

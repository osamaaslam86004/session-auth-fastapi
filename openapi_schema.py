from fastapi.openapi.utils import get_openapi
from main import app


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sesion Auth",
        version="1.0.0",
        description="Cookie Sesion Auth With fastapi_users",
        routes=app.routes,
    )
    # Modify the OpenAPI schema to remove local_kwarg
    for path in openapi_schema["paths"]:
        if "/auth/register" in path:
            # Remove any undesired query parameters
            openapi_schema["paths"][path]["post"]["parameters"] = [
                param
                for param in openapi_schema["paths"][path]["post"]["parameters"]
                if param["name"] != "local_kw"
            ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

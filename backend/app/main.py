from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from app import create_app
import security

app = create_app()

# Add security schemes for Swagger UI
app.openapi_components = {
    "securitySchemes": {
        "bearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter 'Bearer' [space] and then your token in the text input below.\nExample: Bearer eyJhbGciOiJIUzI1NiIsIn..."
        }
    }
}

# Add CSRF middleware
app.add_middleware(security.CSRFMiddleware)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from app import create_app
from security import auth

app = create_app()
auth.handle_errors(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


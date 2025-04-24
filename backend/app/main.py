
import uvicorn
from app import create_app
from security import auth

app = create_app()
auth.handle_errors(app)


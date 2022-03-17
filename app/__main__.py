import uvicorn
from .main import api

if __name__ == "__main__":
    uvicorn.run(app=api, port=3000)

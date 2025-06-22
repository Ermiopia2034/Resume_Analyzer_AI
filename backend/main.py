from fastapi import FastAPI
from auth import router as auth_router
from upload import router as upload_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Analyzer API"}
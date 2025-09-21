from fastapi import FastAPI, APIRouter

base_router = APIRouter(
    
)

@base_router.get("/welcome")
def read_root():
    return {"Hello": "World"}

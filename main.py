from fastapi import FastAPI
from db.database import engine, Base
from middleware.logging import LoggingMiddleware
from routers import user, category, todo


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TODO MANAGEMENT SYSTEM",
    version="1.0.0",
)

app.add_middleware(LoggingMiddleware)

app.include_router(user.router)
app.include_router(category.router)
app.include_router(todo.router)

@app.get("/", tags=["Health Check"])
def root():
    return {"TODO MANAGEMENT SYSTEM IS RUNNING SUCCESSFULLY!"}
from contextlib import asynccontextmanager
import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from controllers.archived_controller import sync_archive
from controllers.inventory_controller import sync_inventory
from controllers.product_controller import check_product_status
from db.database import SessionLocal
from views.product_routers import router as product_router
from views.category_routers import router as category_router
from views.inventory_routers import router as inventory_router
from frontend.frontend_routers import router as frontend_router


def background_sync_loop():
    """Runs checker, inventory sync, and archive sync every 5 seconds."""
    while True:
        db = SessionLocal()
        try:
            check_product_status(db)
            sync_inventory(db)
            sync_archive(db)
        finally:
            db.close()

        time.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=background_sync_loop, daemon=True)
    thread.start()
    yield


app = FastAPI(
    title="Bazar Kori",
    description="This is a grocery shopping application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/ProductImages", StaticFiles(directory="ProductImages"), name="ProductImages"
)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

app.include_router(frontend_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(inventory_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

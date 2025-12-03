from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from controllers.search_controller import SearchController
from controllers.filter_controller import FilterController
import os


class BazarKoriApp:

    def __init__(self):
        self.app = FastAPI(
            title="Bazar Kori E-Commerce API",
            description="Search and Filter Products - MVC Architecture",
            version="1.0.0",
            docs_url="/api/docs",  # Added for Swagger UI
            redoc_url="/api/redoc"  # Added for ReDoc
        )
        self.search_controller = SearchController()
        self.filter_controller = FilterController()

        self.fun_setup_middleware()
        self.fun_setup_routes()
        self.fun_setup_static_files()
        self.fun_setup_html_routes()

    def fun_setup_middleware(self):
        """Allow frontend to talk to backend"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def fun_setup_routes(self):
        """API endpoints"""
        self.app.include_router(self.search_controller.router)
        self.app.include_router(self.filter_controller.router)

    def fun_setup_static_files(self):
        """Serve CSS, JS, images at /static/..."""
        views_path = os.path.join(os.path.dirname(__file__), "views")
        if os.path.exists(views_path):
            self.app.mount("/static", StaticFiles(directory=views_path), name="static")
        else:
            print("Warning: 'views' folder not found!")

    def fun_setup_html_routes(self):
        """Serve the two HTML pages"""

        # Home page → search page
        @self.app.get("/", response_class=HTMLResponse)
        async def serve_search_page():
            file_path = os.path.join(os.path.dirname(__file__), "views", "search.html")
            if not os.path.exists(file_path):
                return HTMLResponse("search.html not found", status_code=404)
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        # Filter/Browse page
        @self.app.get("/filter", response_class=HTMLResponse)
        async def serve_filter_page():
            file_path = os.path.join(os.path.dirname(__file__), "views", "filter.html")
            if not os.path.exists(file_path):
                return HTMLResponse("filter.html not found", status_code=404)
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

    def fun_get_app(self):
        return self.app


# Factory
def fun_create_app():
    app = BazarKoriApp()
    return app.fun_get_app()


app = fun_create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
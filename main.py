from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from controllers.search_controller import SearchController
import os


class BazarKoriApp:
    
    def __init__(self):
        self.app = FastAPI(
            title="Bazar Kori E-Commerce API",
            description="Search Products Feature - MVC Architecture",
            version="1.0.0"
        )
        self.search_controller = SearchController()
        self.fun_setup_middleware()
        self.fun_setup_routes()
        self.fun_setup_static_files()
        self.fun_setup_html_route()
    
    
    def fun_setup_middleware(self):
        """
        Setup CORS and other middleware
        """
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    
    def fun_setup_routes(self):
        """
        Register all route controllers
        """
        self.app.include_router(self.search_controller.router)
    
    
    def fun_setup_static_files(self):
        """
        Setup static files serving
        """
        if os.path.exists("views"):
            self.app.mount("/static", StaticFiles(directory="views"), name="static")
    
    
    def fun_setup_html_route(self):
        """
        Setup route to serve search.html
        """
        @self.app.get("/", response_class=HTMLResponse)
        async def fun_serve_search_page():
            with open("views/search.html", "r") as html_file:
                return html_file.read()
    
    
    def fun_get_app(self):
        """
        Get FastAPI application instance
        """
        return self.app


# Application Factory
def fun_create_app():
    bazar_kori_app = BazarKoriApp()
    return bazar_kori_app.fun_get_app()


app = fun_create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True
    )
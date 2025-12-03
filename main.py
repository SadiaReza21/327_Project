from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controller.admin_login_controller import AdminLoginController
from controller.buyer_signup_controller import BuyerSignupController
from controller.buyer_login_controller import BuyerLoginController
from controller.edit_profile_controller import EditProfileController
from model.buyer import Buyer

app = FastAPI()
templates = Jinja2Templates(directory="view")

admin_login_controller = AdminLoginController()
buyer_signup_controller = BuyerSignupController()
buyer_login_controller = BuyerLoginController()
edit_profile_controller = EditProfileController()


@app.get("/admin-login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    """
    Render the admin login page.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        HTMLResponse: The rendered Admin_Login.html template.
    """
    return templates.TemplateResponse("Admin_Login.html", {"request": request})


@app.post("/admin-login")
def admin_login(request: Request, email: str = Form(...), password: str = Form(...)):
    """
    Authenticate admin and redirect to dashboard if successful.

    Args:
        request (Request): The FastAPI request object.
        email (str): Admin email from form input.
        password (str): Admin password from form input.

    Returns:
        HTMLResponse or RedirectResponse: Renders login template with
        success/failure message or redirects to admin dashboard.
    """
    result = admin_login_controller.login(email, password)
    
    if result["success"]:
        return RedirectResponse(url="http://127.0.0.1:8003/", status_code=303)

    return templates.TemplateResponse(
        "Admin_Login.html",
        {"request": request, "success": result["success"], "message": result["message"]}
    )


@app.get("/buyer-signup", response_class=HTMLResponse)
def buyer_signup_page(request: Request):
    """
    Calls the buyer signup page.

    Args:
        request (Request): The FastAPI requests object.

    Returns:
        HTMLResponse: The Buyer_Signup.html template.
    """
    return templates.TemplateResponse("Buyer_Signup.html", {"request": request})


@app.post("/buyer-signup")
def buyer_signup(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """
    Handle buyer registration.

    Args:
        request (Request): The FastAPI request object.
        name (str): Buyer's name.
        phone (str): Buyer's phone.
        email (str): Buyer's email.
        password (str): Buyer's password.

    Returns:
        HTMLResponse: Calls signup template with success/error message.
    """
    result = buyer_signup_controller.signup(name, phone, email, password)
    return templates.TemplateResponse(
        "Buyer_Signup.html",
        {
            "request": request,
            "success": result.get("status") == "success",
            "message": result.get("message")
        }
    )


@app.get("/buyer-login", response_class=HTMLResponse)
def buyer_login_page(request: Request):
    """
    Calls the buyer login page.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        HTMLResponse: The  Buyer_Login.html template.
    """
    return templates.TemplateResponse("Buyer_Login.html", {"request": request})


@app.post("/buyer-login")
def buyer_login(request: Request, email: str = Form(...), password: str = Form(...)):
    """
    Authenticate buyer and redirect to profile page if successful.

    Args:
        request (Request): The FastAPI request object.
        email (str): Buyer's email from form input.
        password (str): Buyer's password from form input.

    Returns:
        HTMLResponse or RedirectResponse: Renders login template with
        success/failure message or redirects to buyer profile page.
    """
    result = buyer_login_controller.login(email, password)
    
    if result.get("success") and result.get("id"):
        buyer_id = result["id"]
        return RedirectResponse(url=f"http://127.0.0.1:8001/home/{buyer_id}", status_code=303)
 
    return templates.TemplateResponse(
        "Buyer_Login.html",
        {"request": request, "success": result.get("success", False), "message": result.get("message", "Login failed")}
    )


@app.get("/buyer-profile/{id}", response_class=HTMLResponse)
def buyer_profile_page(request: Request, id: int):
    """
    Display buyer profile page.

    Args:
        request (Request): The FastAPI request object.
        id (int): Buyer's ID.

    Returns:
        HTMLResponse or RedirectResponse: Renders profile page or redirects
        to login page if buyer data cannot be fetched.
    """
    buyer_model = Buyer()
    buyer_data = buyer_model.get_buyer(id)
    
    if buyer_data.get("status") == "error":
        return RedirectResponse(url="/buyer-login", status_code=303)
    
    return templates.TemplateResponse(
        "Buyer_Profile.html", 
        {
            "request": request,
            "id": id,
            "name": buyer_data.get("name", ""),
            "phone": buyer_data.get("phone", ""),
            "email": buyer_data.get("email", "")
        }
    )


@app.post("/update-profile/{id}")
def profile_edit(request: Request, id: int, name: str = Form(...), phone: str = Form(...)):
    """
    Update buyer profile information.

    Args:
        request (Request): The FastAPI request object.
        id (int): Buyer's ID.
        name (str): Updated name.
        phone (str): Updated phone.

    Returns:
        HTMLResponse: Renders buyer profile page with success/error message.
    """
    result = edit_profile_controller.edit_profile(id, name, phone)
    buyer_model = Buyer()
    buyer_data = buyer_model.get_buyer(id)
    
    return templates.TemplateResponse(
        "Buyer_Profile.html",
        {
            "request": request,
            "id": id,
            "name": buyer_data.get("name", name),
            "phone": buyer_data.get("phone", phone),
            "email": buyer_data.get("email", ""),
            "success": result.get("status") == "success",
            "message": result.get("message", "")
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)

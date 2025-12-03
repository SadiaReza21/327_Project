from model.admin import Admin

class AdminLoginController:
    def __init__(self):
        self.admin_model = Admin()
    
    def login(self, email, password):
        """
        Authenticate an admin using email and password.

        Checks the provided credentials against the Admin model's authentication
        method and returns a response indicating the result.

        Args:
            email (str): The admin's email address.
            password (str): The admin's password in plaintext.

        Returns:
            dict: A dictionary containing:
                - ``success`` (bool): Whether login was successful.
                - ``message`` (str): A message describing the outcome.
        """

        if self.admin_model.authenticate(email, password):
            return {"success": True, "message": "Login successful"}
        else:
            return {"success": False, "message": "Invalid email or password"}
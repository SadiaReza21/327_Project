from model.buyer import Buyer

class BuyerLoginController:
    def __init__(self):
        self.buyer_model = Buyer()

    def login(self, email: str, password: str):
        """
        Authenticate a buyer using email and password.

        Calls the Buyer model's authentication method and returns a dictionary
        indicating the login result. If authentication succeeds, the buyer's
        basic details are included in the response.

        Args:
            email (str): The buyer's email address.
            password (str): The buyer's password in plaintext .

        Returns:
            dict: A dictionary containing:
                - ``success`` (bool): Whether login was successful.
                - ``message`` (str): Status message describing the outcome.
                - ``id`` (int, optional): Buyer's ID (only if login is successful).
                - ``email`` (str, optional): Buyer's email (only if login is successful).
        """
        result = self.buyer_model.authenticate(email, password)
        
        if isinstance(result, dict) and result.get("success"):
            return {
                "success": True, 
                "message": "Login successful",
                "id": result.get("id"),
                "email": result.get("email")
            }
        else:
            return {"success": False, "message": "Invalid email or password"}
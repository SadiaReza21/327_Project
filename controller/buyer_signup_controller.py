from model.buyer import Buyer

class BuyerSignupController:
    def __init__(self):
        self.buyer_model = Buyer()

    def signup(self, name: str, phone: str, email: str, password: str):
        """
        Register a new buyer.

        Validates the input fields and sends the data to the Buyer model 
        for account creation. Returns a status message based on whether the 
        signup was successful or failed.

        Args:
            name (str): Full name of the buyer.
            phone (str): Buyer's phone number.
            email (str): Buyer's email address.
            password (str): Buyer's password in plaintext.

        Returns:
            dict: A dictionary containing:
                - ``status`` (str): "success" or "error".
                - ``message`` (str): Description of the result.
        """
        
        if not name or not phone or not email or not password:
            return {"status": "error", "message": "All fields are required"}
        
        result = self.buyer_model.signup(name.strip(), phone.strip(), email.strip(), password.strip())
        return result

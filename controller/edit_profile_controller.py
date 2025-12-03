from model.buyer import Buyer

class EditProfileController:
    def __init__(self):
        self.buyer_model = Buyer()

    def edit_profile(self, id, name: str, phone: str):
        """
        Update a buyer's profile information.

        Validates the required fields and then calls the Buyer model to update 
        the buyer's name and phone number.

        Args:
            id (int): The buyer's unique ID.
            name (str): The updated full name of the buyer.
            phone (str): The updated phone number of the buyer.

        Returns:
            dict: A dictionary containing:
                - ``status`` (str): "success" or "error".
                - ``message`` (str): Description of the update result.
        """
        
        if not name or not phone:
            return {"status": "error", "message": "All fields are required"}
        
        result = self.buyer_model.edit_profile(name, phone)
        return result
from app.models.db_actions import OrderDbQueries
class Orders:
    """
    This class handles menu object creation
    """
    def __init__(self,email="", menu_id="", status=""):
        self.email= email
        self.status = "new"
        self.menu_id = menu_id

    def create_order(self):
        """
        This method calls the place method from the database class
        to place an order in the database
        """
        OrderDbQueries().place_order(self)
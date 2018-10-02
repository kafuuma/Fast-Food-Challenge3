from app.models.db_actions import OrderDbQueries
class Orders:
    """This class handles all orders, creation and storage"""
    def __init__(self,email="", menu_id="", status=""):
        self.email= email
        self.status = "new"
        self.menu_id = menu_id

    def create_order(self):
       OrderDbQueries().place_order(self)
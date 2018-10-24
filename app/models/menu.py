from app.models.db_actions import MenuDbQueries


class Menu:
    """
    This is a menu class, it handles menu object creation
    """
    def __init__(self,menu_name="", description="", price="",menu_image=""):
        self.menu_name = menu_name
        self.description = description
        self.menu_price = price
        self.menu_image = menu_image
        
    def add_menu_item(self):
        """
        This method calls the menu database create menu method
        to put a menu item in the database
        """
        MenuDbQueries().create_menu_item(self)
    


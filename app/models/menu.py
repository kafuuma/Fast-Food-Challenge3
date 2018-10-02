from app.models.db_actions import MenuDbQueries


class Menu:
    """This class does all the menu related stuff"""
    def __init__(self,menu_name="", description="", price=""):
        self.menu_name = menu_name
        self.description = description
        self.menu_price = price
        
    def add_menu_item(self):
        MenuDbQueries().create_menu_item(self)
    


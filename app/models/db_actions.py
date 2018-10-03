import psycopg2
import psycopg2.extras as e
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os


class Database:
    """This class does connection of the database to the application"""

    def __init__(self,password="#kafuuma#"):
        try:
            if os.getenv("app_settings") == "testing":
                dbname = "testffood"
            else:
                dbname = "ffood"
            self.conn = psycopg2.connect(
                """dbname='{}' user='postgres' password='{}' host='localhost' port='5432'
                """.format(dbname,password)
            )
            self.cur = self.conn.cursor(cursor_factory=e.DictCursor)
            print("connected to database {}".format(dbname))
            print(os.getenv("app_settings"))
        except:
            print("Failed to connect to database")
    
class UserDbQueries(Database):
    """This class inherits from the database class, it does creation and 
    insertion of user data into the database, plus all data manipulation"""

    def __init__(self):
        Database.__init__(self)
    
    def create_table(self):
        """This method creates a user table in the database"""
        sql = (
            """CREATE TABLE IF NOT EXISTS users(user_id serial PRIMARY KEY, full_name varchar(100), 
            email varchar(100) UNIQUE, password varchar(300), contact varchar(20), user_role varchar(10));"""
        )
        self.cur.execute(sql)
        self.conn.commit()

    def create_user(self, user):
        """This method inserts a user into a user table in the database"""
        sql =(
            """INSERT INTO users (full_name , email, password, contact, user_role) 
            VALUES('{}','{}','{}','{}','{}');
            """.format(user.full_name, user.email, 
                generate_password_hash(user.password), user.contact, user.user_role)
            )
        self.cur.execute(sql)
        self.conn.commit()

    def fetch_user(self, user):
        """This method fetches a user from the database"""
        sql =(
            """SELECT * FROM users WHERE email = '{}';
            """.format(user.email)
            )
        self.cur.execute(sql)
        return self.cur.fetchall()
       
    def delete_user(self, user_id):
        """This method fetches a user from the database by Id"""
        sql = (
            """
            DELETE FROM users WHERE user_id = '{}'
            """.format(user_id)
            )
        self.cur.execute(sql)
        self.conn.commit()


    def change_user_role(self,role, user_id):
        """This method updates a user role in the database"""
        sql = (
            """
            UPDATE users SET user_role = '{}' WHERE user_id = '{}'
            """.format(role, user_id)
        )
        self.cur.execute(sql)
        self.conn.commit()

    def drop_table(self):
        """This method deletes a table from the database"""
        sql = ("""DROP TABLE users""")
        self.cur.execute(sql)
        self.conn.commit()

class MenuDbQueries(Database):
    def __init__(self):
        Database.__init__(self)

    def create_table(self):
        sql = (
            """CREATE TABLE IF NOT EXISTS menu (menu_id serial PRIMARY KEY ,
            menu_name varchar(100) UNIQUE, menu_price REAL, description varchar(200));
            """
        )
        self.cur.execute(sql)
        self.conn.commit()

    def create_menu_item(self,menu):
        sql =(
            """INSERT INTO menu (menu_name, menu_price,  description ) 
            VALUES('{}','{}','{}');
            """.format(menu.menu_name,menu.menu_price, menu.description)
        )
        self.cur.execute(sql)
        self.conn.commit()
    
    def fetch_all_menu(self):
        sql =(
            """SELECT * FROM menu 
            """
        )
        self.cur.execute(sql)
        output = self.cur.fetchall()
        return self.convert_output_to_dict(output)

    def fetch_menu(self, menu):
       
        sql =(
            """SELECT * FROM menu WHERE menu_name ='{}' 
            """.format(menu.menu_name)
        )
        self.cur.execute(sql)
        output = self.cur.fetchall()
        return self.convert_output_to_dict(output)
    
    def convert_output_to_dict(self, output):
        menu = []
        for menu_item in output:
            result = {
                "menu_id": menu_item["menu_id"],
                "menu_name": menu_item["menu_name"],
                "menu_price": menu_item["menu_price"],
                "description": menu_item["description"]
              }
            menu.append(result)
        return menu


    def delete_menu(self, menu_id):
        sql = (
            """
            DELETE from menu WHERE menu_id = '{}'
            """.format(menu_id)
        )
        self.cur.execute(sql)
        self.conn.commit()

    def drop_table(self):
        sql = ("""DROP TABLE menu""")
        self.cur.execute(sql)
        self.conn.commit()

class OrderDbQueries(Database):

    def __init__(self):
        Database.__init__(self)
    def create_table(self):
        sql = (
            """CREATE TABLE IF NOT EXISTS orders (order_id serial PRIMARY KEY,
            menu_id INTEGER NOT NULL REFERENCES menu(menu_id) ON DELETE CASCADE,
            email varchar(100) NOT NULL, status varchar(20), 
            ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );
            """
        )
        self.cur.execute(sql)
        self.conn.commit()
    

    def place_order(self, order):  
        """ use order object insted"""
        sql = (
            """INSERT INTO orders (menu_id, email, status) VALUES ('{}', '{}', '{}')
            """.format(order.menu_id, order.email, order.status)
        )
        self.cur.execute(sql)
        self.conn.commit()
    
    def fetch_all_orders(self):
        sql = (
            """SELECT * FROM orders"""
        )
        self.cur.execute(sql)
        output = self.cur.fetchall()
        return self.convert_output_to_dict(output)

    def fetch_order(self, email, menu_id):
        sql = (
            """
            SELECT * FROM orders WHERE email = '{}' AND menu_id = '{}'
            """.format(email, menu_id)
        )
        self.cur.execute(sql)
        output = self.cur.fetchall()
        return self.convert_output_to_dict(output)
        
    
    def fetch_orders(self, email):
        sql = (
            """
            SELECT * FROM orders WHERE email = '{}'
            """.format(email)
         )
        self.cur.execute(sql)
        output = self.cur.fetchall()
        return self.convert_output_to_dict(output)



    def fetch_order_byId(self,orde_id):
        sql = (
            """
            SELECT * FROM orders WHERE order_id = '{}'
            """.format(orde_id)
        )
        self.cur.execute(sql)
        output= self.cur.fetchall()
        return self.convert_output_to_dict(output)

    def convert_output_to_dict(self, output):
        orders = []
        for order in output:
            result = {
                "order_id": order["order_id"],
                "menu_id": order["menu_id"],
                "email": order["email"],
                "status": order["status"],
                # "ordered_at": order["ordered_at"]
                }
            orders.append(result)
        return orders

    def update_order_status(self, order_id, status):
        sql = (
            """
            UPDATE orders SET status = '{}' WHERE order_id = '{}'
            """.format(status, order_id)
        )
        self.cur.execute(sql)
        self.conn.commit()

    def drop_table(self):
        sql = ("""DROP TABLE orders""")
        self.cur.execute(sql)
        self.conn.commit()


# dbuser = UserDbQueries()
# dbuser.create_table()
# dbmenu = MenuDbQueries()
# dbmenu.create_table()
# dborder = OrderDbQueries()
# dborder.create_table()


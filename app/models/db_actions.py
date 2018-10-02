import psycopg2
import psycopg2.extras as e
from werkzeug.security import check_password_hash, generate_password_hash
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
        self.instance = Database.__init__(self)
    
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




from datetime import datetime
from food_review import bcrypt

class User(object):
    def __init__(self, mysql, user_data=None):
        self.mysql = mysql
        
        self.id = 0
        self.username = user_data['username'] if not user_data == None else None
        self.email = user_data['email'] if not user_data == None else None
        self.name = user_data['name'] if not user_data == None else None
        self.password = user_data['password'] if not user_data == None else None
        self.created_at = None
        self.is_writer = user_data['is_writer'] if not user_data == None else False

    def save(self):
        hashed = bcrypt.generate_password_hash(self.password).decode('utf-8')

        query = '''INSERT INTO users (`username`, `email`, `password`, `name`, `is_writer`)
            values ("{}", "{}", "{}", "{}", "{}")'''.format(self.username, self.email, 
            hashed, self.name, self.is_writer)
        
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)

        self.mysql.connection.commit()

    def get(self, id):
        query = 'SELECT * FROM users WHERE id={}'.format(id)

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

        return result

    def all(self):
        query = 'SELECT * FROM users'

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    def login(self, cred):
        query = 'SELECT * FROM users WHERE username="{}" OR email="{}"'.format(
            cred['username'], cred['username'])

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

        if result and bcrypt.check_password_hash(result['password'], 
            cred['password']):
            return result
            
        return False

class Review(object):
    def __init__(self, mysql, review_data=None):
        self.mysql = mysql
        
        self.id = 0
        self.content = review_data['content'] if not review_data == None else None
        self.rating = review_data['rating'] if not review_data == None else None
        self.user_id = review_data['user_id'] if not review_data == None else None
        self.recipe_id = review_data['recipe_id'] if not review_data == None else None
        self.created_at = None

    def save(self):
        query = '''INSERT INTO reviews (`content`, `rating`, `user_id`, `recipe_id`)
            VALUES ("{}", "{}", "{}", "{}")'''.format(self.content, self.rating, 
            self.user_id, self.recipe_id)
        
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)

        self.mysql.connection.commit()

    def get_from_recipe(self, id):
        query = 'SELECT * FROM reviews WHERE recipe_id = {}'.format(id)

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        for res in result:
            res['user'] = User(self.mysql).get(res['user_id'])

        return result

    def all(self): 
        query = 'SELECT * FROM reviews'

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result

class Recipe(object):
    def __init__(self, mysql, recipe_data=None):
        self.mysql = mysql

        self.id = 0
        self.name = recipe_data['name'] if not recipe_data == None else None
        self.description = recipe_data['description'] if not recipe_data == None else None
        self.img_path = recipe_data['img_path'] if not recipe_data == None else None
        self.user_id = recipe_data['user_id'] if not recipe_data == None else None
        self.writer = None
        self.created_at = None
        
    def save(self):
        query = '''INSERT INTO recipes (`name`, `description`, `user_id`, `img_path`)
            VALUES ("{}", "{}", "{}", "{}")'''.format(self.name, self.description, 
            self.user_id, self.img_path)
        
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)

        self.mysql.connection.commit()

        return self.get(cursor.lastrowid)

    def all(self): 
        query = 'SELECT * FROM recipes'

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        for res in result:
            res['writer'] = User(self.mysql).get(res['user_id'])

        return result

    def get(self, id):
        query = 'SELECT * FROM recipes WHERE id={}'.format(id)

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

        result['writer'] = User(self.mysql).get(result['user_id'])
        result['reviews'] = list(Review(self.mysql).get_from_recipe(result['id']))

        return result

class Ingredient(object):
    def __init__(self, mysql, ingredient_data=None):
        self.id = 0
        self.food_id
        self.component
        self.measure

    def sana_all(self): 
        query = 'SELECT * FROM ingredient'

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result
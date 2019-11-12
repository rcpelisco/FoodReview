from datetime import datetime
from food_review import bcrypt

class LoginCredentials(object):
    def __init__(self, mysql, login_cred_data=None):
        self.mysql = mysql

        self.id = 0
        self.username = login_cred_data['username'] if not login_cred_data == None else None
        self.password = login_cred_data['password'] if not login_cred_data == None else None
        self.user_id = login_cred_data['user_id'] if not login_cred_data == None else None

    def save(self):
        hashed = bcrypt.generate_password_hash(self.password).decode('utf-8')

        query = '''INSERT INTO login_credentials (`username`, `password`, `user_id`)
            values ("{}", "{}", "{}")'''.format(self.username, hashed, self.user_id)
        
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)

        self.mysql.connection.commit()

    def login(self, cred):
        query = 'SELECT * FROM login_credentials WHERE username="{}"'.format(
            cred['username'])

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
        if result and bcrypt.check_password_hash(result['password'], 
            cred['password']):
            return result
            
        return False

class User(object):
    def __init__(self, mysql, user_data=None):
        self.mysql = mysql
        
        self.id = 0
        self.first_name = user_data['first_name'] if not user_data == None else None
        self.middle_name = user_data['middle_name'] if not user_data == None else None
        self.last_name = user_data['last_name'] if not user_data == None else None
        self.address = user_data['address'] if not user_data == None else None
        self.phone_number = user_data['phone_number'] if not user_data == None else None
        self.email_address = user_data['email_address'] if not user_data == None else None
        self.created_at = None
        self.user_type_id = user_data['user_type_id'] if not user_data == None else False

    def save(self):
        query = '''INSERT INTO users (`first_name`, `middle_name`, `last_name`, 
            `address`, `phone_number`, `email_address`, `user_type_id`)
            values ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'''.format(self.first_name, 
            self.middle_name, self.last_name, self.address, self.phone_number, 
            self.email_address, self.user_type_id)
        
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)

        self.mysql.connection.commit()

        return self.get(cursor.lastrowid)

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
            res['comments'] = list(Comment(self.mysql).get_from_review(res['id']))
            print(res)

        return result

    def all(self): 
        query = 'SELECT * FROM reviews'

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result

class Comment(object):
    def __init__(self, mysql, comment_data=None):
        self.mysql = mysql

        self.id = 0
        self.content = comment_data['content'] if not comment_data == None else None
        self.user_id = comment_data['user_id'] if not comment_data == None else None
        self.review_id = comment_data['review_id'] if not comment_data == None else None
        self.created_at = None

    def save(self):
        query = '''INSERT INTO comments (`content`, `user_id`, `review_id`)
            VALUES ("{}", "{}", "{}")'''.format(self.content, self.user_id, 
            self.review_id)
        
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)

        self.mysql.connection.commit()

    def get_from_review(self, review_id):
        query = 'SELECT * FROM comments WHERE review_id = {}'.format(review_id)

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        for res in result:
            res['user'] = User(self.mysql).get(res['user_id'])
            
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
        result['ingredients'] = list(Ingredient(self.mysql).get_from_recipe(result['id']))
        
        return result

class Ingredient(object):
    def __init__(self, mysql, ingredient_data=None):
        self.mysql = mysql

        self.id = 0
        self.recipe_id = ingredient_data['recipe_id'] if not ingredient_data == None else None
        self.component = ingredient_data['component'] if not ingredient_data == None else None
        self.measure = ingredient_data['measure'] if not ingredient_data == None else None

    def get(self, id):
        query = 'SELECT * FROM ingredients WHERE id = {}'.format(id)

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    def get_from_recipe(self, id):
        query = 'SELECT * FROM ingredients WHERE recipe_id = {}'.format(id)

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    def sana_all(self): 
        query = 'SELECT * FROM ingredient'

        cursor = self.mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    def save(self):
        query = '''INSERT INTO ingredients (`component`, `measure`, `recipe_id`)
            VALUES ("{}", "{}", "{}")'''.format(self.component, self.measure, 
            self.recipe_id)
        
        cursor = self.mysql.connection.cursor()
        cursor.execute(query)

        self.mysql.connection.commit()

        return self.get(cursor.lastrowid)

    
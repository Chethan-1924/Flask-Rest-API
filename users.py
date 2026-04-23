from flask import Flask,jsonify,request
from db import get_db_connection

def register_user_routes(app):
    # ADD user [POST] == (CREATE)
    @app.route('/users',methods=['POST'])
    def add_user():

        data = request.get_json()

        if not data:
            return jsonify({"error": "Request must be JSON"}), 400

        name = data.get("name")
        age = data.get("age")

        # Validating name:
        if not name:
            return jsonify({"error":"Name is equired"}),400
        
        if not isinstance(name,str):
            return jsonify({"error":"name must be a string"}),400
        
        if len(name.strip()) < 2:
            return jsonify({"error":"Name must be aleast 2 characters"}),400
        
        if not name.replace(" ","").isalpha():
            return jsonify({"error": "Name must contain only alphabets"}), 400
        
        # Validating age:
        if not age:
            return jsonify({"error":"Age is equired"}),400
            
        if not isinstance(age,int):
            return jsonify({"error":"Age must be a number"}),400
        
        if age < 1 or age >120:
            return jsonify({"error":"Age must be between 1 and 120"}),400


        db = get_db_connection()
        cursor = db.cursor()

        query = "insert into users (name,age) values (%s, %s)"
        values = (name,age)

        cursor.execute(query,values)
        db.commit()

        return jsonify({"message": "user added successfully"})


    # Fetching data from SQL,  [GET] == [READ]
    @app.route('/users',methods=['GET'])
    def get_users():

        db = get_db_connection()
        cursor = db.cursor()

        query = "select * from users"
        cursor.execute(query)

        Result = cursor.fetchall()

        users = []

        for row in Result:
            user = {
                "id": row[0],
                "name": row[1],
                "age":row[2]
            }
            users.append(user)

        return jsonify(users)


    # fetch users using user id ,[GET] == (READ)
    @app.route('/users/<int:user_id>',methods=['GET'])
    def get_user(user_id):

        db = get_db_connection()
        cursor = db.cursor()

        # Validating USER ID:
        if user_id <= 0:
            return jsonify({"error":"Invalid user ID"}),400
        

        query = "select * from users where id = %s"
        cursor.execute(query,(user_id,))
        
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error":"user not found"}),404
        
        user = {
            "id":result[0],
            "name":result[1],
            "age":result[2]
        }

        return jsonify(user)


    # Update the user data,   [PUT]==(UPDATE)

    @app.route("/users/<int:user_id>",methods=['PUT'])
    def update_user(user_id):

        # Validating the ID:
        if user_id <= 0:
            return jsonify({"error":"Invalid user ID"}),400
        
        data = request.get_json()
        # Check JSON
        if not data:
            return jsonify({"error":"Request body must be JSON"}),400
        
        name = data.get("name")
        age = data.get("age")

        # Validating name:
        if not name:
            return jsonify({"error":"Name is equired"}),400
        
        if not isinstance(name,str):
            return jsonify({"error":"name must be a string"}),400
        
        if len(name.strip()) < 2:
            return jsonify({"error":"Name must be aleast 2 characters"}),400
        
        if not name.replace(" ","").isalpha():
            return jsonify({"error": "Name must contain only alphabets"}), 400
        
        # Validating age:
        if not age:
            return jsonify({"error":"Age is equired"}),400
            
        if not isinstance(age,int):
            return jsonify({"error":"Age must be a number"}),400
        
        if age < 1 or age >120:
            return jsonify({"error":"Age must be between 1 and 120"}),400
        
        
        db = get_db_connection()
        cursor = db.cursor()


        query  = "update users set name = %s, age = %s where id = %s"
        values = (name,age,user_id)

        cursor.execute(query,values)
        db.commit()

        # If no user is inserted
        if cursor.rowcount == 0:
            return jsonify({"error":"user not found"}),404
        
        return jsonify({"message": "user updated successfully"})



    # Deleting a user data,  (DELETE)
    @app.route("/users/<int:user_id>",methods=["DELETE"])
    def delete_user(user_id):
        
        db = get_db_connection()
        cursor = db.cursor()

        query = "delete from users where id = %s"
        cursor.execute(query,(user_id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error":"user not found"}),404
        
        return jsonify({"message":"user deleted successfully"})

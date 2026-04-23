from flask import Flask, jsonify, request
import mysql.connector
from users import register_user_routes


app = Flask(__name__)  # set default configurations

register_user_routes(app)

@app.route('/')
def home():
    return jsonify({"message": "API is working!"})

if __name__ == "__main__":
    app.run(debug=True)
     
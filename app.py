from flask import Flask,request
from flask import jsonify
import os
import psycopg
from dotenv import load_dotenv
load_dotenv()

host =os.getenv("DB_HOST")
dbname =os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")

app =Flask(__name__)
def database():
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor= conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users
                   (
                       id SERIAL PRIMARY KEY,
                       name TEXT,
                       email TEXT UNIQUE,
                       password TEXT,
                       role TEXT
                       )
                       """)
    conn.commit()
    print("Database connected successfully")
    conn.close()
database()

#post user route ----------------------
@app.route("/api/users", methods=["POST"])
def post_users():
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor = conn.cursor()
    data= request.get_json()
    if not data.get("name") or not data.get("email") or not data.get("password") or not data.get("role"):
        return jsonify({"message":"all fields required"}),400
    name = data["name"]
    email = data["email"]
    user_password= data["password"]
    role=data["role"]
    try:
        cursor.execute("INSERT INTO users(name,email,password,role) VALUES(%s,%s,%s,%s)",(name,email,user_password,role))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"user inserted successfully"}),200

#get user route ----------------
@app.route("/api/users", methods=["GET"])
def get_users():
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        users=cursor.fetchall()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify(users),200

app.run(debug=True)
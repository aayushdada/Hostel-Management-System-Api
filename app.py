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
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS hostels
                (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    address TEXT,
                    total_rooms INTEGER
                )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS rooms(
                       id SERIAL PRIMARY KEY,
                       hostel_id INTEGER REFERENCES hostels(id),
                       room_number INTEGER,
                       capacity INTEGER,
                       price INTEGER,
                       status TEXT
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


#get only one user route ---------------------
@app.route("/api/users/<int:id>", methods=["GET"])
def get_one_user(id):
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor= conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE id=%s",(id,))
        existing_user=cursor.fetchone()
        if not existing_user:
            return jsonify({"message":"user does not exist"}),404
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify(existing_user)

#put user route -------------------
@app.route("/api/users/<int:id>", methods=["PUT"])
def update_user(id):
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor = conn.cursor()
    data= request.get_json()
    if not data.get("name") or not data.get("email") or not data.get("password") or not data.get("role"):
        return jsonify({"message":"all fields are required"}),400
    try:
        cursor.execute("SELECT * FROM users WHERE id=%s",(id,))
        existing_user=cursor.fetchone()
        if not existing_user:
            return jsonify({"message":"user does not exist"}),404
        name = data["name"]
        email =data["email"]
        user_password=data["password"]
        role = data["role"]
        cursor.execute("UPDATE users SET name=%s,email=%s,password=%s,role=%s WHERE id=%s",(name,email,user_password,role,id))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"sucessfully update"}),200

# patch user route -------------------------
@app.route("/api/users/<int:id>", methods=["PATCH"])
def patch_user(id):
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor = conn.cursor()
    data = request.get_json()
    if not data.get("name") and not data.get("email") and not data.get("password") and not data.get("role"):
        return jsonify({"message":"at least one field is required"}),400
    try:
        cursor.execute("SELECT * FROM users WHERE id=%s",(id,))
        existing_user=cursor.fetchone()
        if not existing_user:
            return jsonify({"message":"user does not exist"}),404
        if "name" in data:
            name = data["name"]
            cursor.execute("UPDATE users SET name=%s WHERE id=%s",(name,id))
        if "email" in data:
            email = data["email"]
            cursor.execute("UPDATE users SET email=%s WHERE id=%s",(email,id))
        if "password" in data:
            user_password = data["password"]
            cursor.execute("UPDATE users SET user_password=%s WHERE id=%s",(password,id))
        if "role" in data:
            role = data["role"]
            cursor.execute("UPDATE users SET role=%s WHERE id=%s",(role,id))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"updated successflly"}),200


#delete user route -----------------------------------------------
@app.route("/api/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor= conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE id=%s",(id,))
        existing_user=cursor.fetchone()
        if not existing_user:
            return jsonify({"message":"user not found"}),404
        cursor.execute("DELETE FROM users WHERE id=%s",(id,))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"deleted successfully"})


#hostels -------------------------
#hostels post route-------------
@app.route("/api/hostels", methods=["POST"])
def post_hostels():
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor= conn.cursor()
    data = request.get_json()
    if not data.get("name") or not data.get("address") or not data.get("total_rooms"):
        return jsonify({"message":"all fields are required"}),400
    try:
        name=data["name"]
        address=data["address"]
        total_rooms=data["total_rooms"]
        cursor.execute("INSERT INTO hostels(name,address,total_rooms) VALUES(%s,%s,%s)",(name,address,total_rooms))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"data inserted succesfully"}),200

#hostel get route ---------------------
@app.route("/api/hostels",methods=["GET"])
def get_hostels():
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor= conn.cursor()
    try:
        cursor.execute("SELECT * FROM hostels")
        hostels=cursor.fetchall()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify(hostels),200

#only one hostel get route ----------
@app.route("/api/hostels/<int:id>", methods=["GET"])
def get_one_hostel(id):
    conn =psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT * FROM hostels WHERE id=%s",(id,))
        existing_hostel=cursor.fetchone()
        if not existing_hostel:
            return jsonify({"message":"hostel does not exist"}),404
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify(existing_hostel),200

#update(put) route
@app.route("/api/hostels/<int:id>", methods=["PUT"])
def update_hostel(id):
    conn= psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    data=request.get_json()
    if not data.get("name") or not data.get("address") or not data.get("total_rooms"):
        return jsonify({"message":"all fields are required"}),400
    try:
        cursor.execute("SELECT * FROM hostels WHERE id=%s",(id,))
        existing_hostel=cursor.fetchone()
        if not existing_hostel:
            return jsonify({"message":"hostel does not exist"}),404
        name=data["name"]
        address=data["address"]
        total_rooms=data["total_rooms"]
        cursor.execute("UPDATE hostels SET name=%s,address=%s,total_rooms=%s WHERE id=%s",(name,address,total_rooms,id))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"updated successfully"}),200

#patch route ---------------
@app.route("/api/hostels/<int:id>", methods=["PATCH"])
def update_one_hostel(id):
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    data= request.get_json()
    if not data.get("name") and not data.get("address") and not data.get("total_rooms"):
        return jsonify({"message":"data must must be inserted"}),400
    try:
        cursor.execute("SELECT * FROM hostels WHERE id=%s",(id,))
        existing_hostel=cursor.fetchone()
        if not existing_hostel:
            return jsonify({"message":"hostel does not exist"}),404
        if "name" in data:
            name=data["name"]
            cursor.execute("UPDATE hostels SET name=%s WHERE id=%s",(name,id))
        if "address" in data:
            address=data["address"]
            cursor.execute("UPDATE hostels SET address=%s WHERE id=%s",(address,id))
        if "total_rooms" in data:
            total_rooms=data["total_rooms"]
            cursor.execute("UPDATE hostels SET total_rooms=%s WHERE id=%s",(total_rooms,id))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"updatd successfully"}),200

#delete hostel route------------------
@app.route("/api/hostels/<int:id>", methods=["DELETE"])
def delete_hostel(id):
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT * FROM hostels WHERE id=%s",(id,))
        existing_hostel=cursor.fetchone()
        if not existing_hostel:
            return jsonify({"message":"hostel does not exist"}),404
        cursor.execute("DELETE FROM hostels WHERE id=%s",(id,))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"deleted successflly"}),200


#rooms route --------------
#post room route --------------
@app.route("/api/rooms", methods=["POST"])
def post_rooms():
    conn= psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    data=request.get_json()
    if not data.get("hostel_id") or not data.get("room_number") or not data.get("capacity") or not data.get("price") or not data.get("status"):
        return jsonify({"message":"all fields required"}),400
    try:
        hostel_id=data["hostel_id"]
        room_number=data["room_number"]
        capacity=data["capacity"]
        price=data["price"]
        status=data["status"]
        cursor.execute("INSERT INTO rooms(hostel_id,room_number,capacity,price,status) VALUES(%s,%s,%s,%s,%s)",(hostel_id,room_number,capacity,price,status))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"data inserted successfully"}),200

#get all rooms route-------------
@app.route("/api/rooms",methods=["GET"])
def get_rooms():
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT * FROM rooms")
        rooms=cursor.fetchall()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify(rooms)
#get only one room
@app.route("/api/rooms/<int:id>", methods=["GET"])
def get_one_room(id):
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT * FROM rooms WHERE id=%s",(id,))
        room=cursor.fetchone()
        if not room:
            return jsonify({"message":"room does not exist"}),404
    except psycopg.OperationalError:
        return jsonify({"message":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify(room)

#update room route ---------------
@app.route("/api/rooms/<int:id>", methods=["PUT"])
def update_room(id):
    conn= psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    data=request.get_json()
    print(data)
    if not data.get("hostel_id") or not data.get("room_number") or not data.get("capacity") or not data.get("price") or not data.get("status"):
        return jsonify({"message":"all fields are required"}),400
    try:
        cursor.execute("SELECT * FROM rooms WHERE id=%s",(id,))
        room=cursor.fetchone()
        if not room:
            return jsonify({"message":"room does not exist"}),404
        hostel_id=data["hostel_id"]
        room_number=data["room_number"]
        capacity=data["capacity"]
        price=data["price"]
        status=data["status"]
        cursor.execute("UPDATE rooms SET hostel_id=%s,room_number=%s,capacity=%s,price=%s,status=%s WHERE id=%s",(hostel_id,room_number,capacity,price,status,id))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"sucessfully updated"}),200

#patch route----------------------
@app.route("/api/rooms/<int:id>", methods=["PATCH"])
def update_one_field(id):
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    data=request.get_json()
    if not data.get("hostel_id") and not data.get("room_number") and not  data.get("capacity") and not data.get("price") and not data.get("status"):
        return jsonify({"message":"data must be inserted"}),400
    try:
        cursor.execute("SELECT * FROM rooms WHERE id=%s",(id,))
        room=cursor.fetchone()
        if not room:
            return jsonify({"message":"room does not exist"}),404
        if "hostel_id" in data:
            hostel_id=data["hostel_id"]
            cursor.execute("UPDATE rooms SET hostel_id=%s WHERE id=%s",(hostel_id,id))
        if "room_number" in data:
            room_number=data["room_number"]
            cursor.execute("UPDATE rooms SET room_number=%s WHERE id=%s",(room_number,id))
        if "capacity" in data:
            capacity=data["capacity"]
            cursor.execute("UPDATE rooms SET capacity=%s WHERE id=%s",(capacity,id))
        if "price" in data:
            price=data["price"]
            cursor.execute("UPDATE rooms SET price=%s WHERE id=%s",(price,id))
        if "status" in data:
            status=data["status"]
            cursor.execute("UPDATE rooms SET status=%s WHERE id=%s",(status,id))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"updated successfully"}),200

#delete route------------------------------
@app.route("/api/rooms/<int:id>", methods=["DELETE"])
def delete_room(id):
    conn = psycopg.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT * FROM rooms WHERE id=%s",(id,))
        room=cursor.fetchone()
        if not room:
            return jsonify({"message":"room does not exist"}),404
        cursor.execute("DELETE FROM rooms WHERE id=%s",(id,))
        conn.commit()
    except psycopg.OperationalError:
        return jsonify({"error":"database error"}),500
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message":"Deleted successfully"}),200

app.run(debug=True)
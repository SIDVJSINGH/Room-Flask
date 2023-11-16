from flask import Flask, render_template, url_for, request, session, redirect
from flask_socketio import SocketIO, emit, leave_room, send, join_room
import random
from string import ascii_lowercase, digits,ascii_uppercase
from datetime import timedelta, datetime
from flask_pymongo import PyMongo
import base64

# from flask_uploads import UploadSet, IMAGES, configure_uploads



app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join(random.choice(ascii_lowercase + digits + ascii_uppercase) for i in range(16))
MAX_BUFFER_SIZE = 100*1000*1000 # 100 MB
socketio = SocketIO(app, max_http_buffer_size=MAX_BUFFER_SIZE)

app.config['MONGO_URI'] ='${{ secrets.MONGODB_URI_SIDVJSINGH }}/chat'
mongo = PyMongo(app)


rooms = {}  #{"room_code": {"members":0, "users": [], "messages": [], "media": []}}

def generate_room_code(length:int):
  while True:
    room_code = ""
    for _ in range(length):
      room_code += random.choice( digits + ascii_uppercase)
    if room_code not in rooms: # if the room_code exist in rooms dict, generate new one
      break
  return room_code

@app.route('/', methods=['GET', 'POST'])
def home():  
  session.clear()
  
  if request.method == 'POST':
    # Session Timeout in 30 minutes
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
     
    name = request.form.get('name')
    join_code = request.form.get('join_code')
    join = request.form.get('join', False) # button
    create = request.form.get('create', False) # button
    
    if not name:
      return render_template("home.html", error_message="Please enter your name", join_code=join_code,name=name)
    
    if join!=False and not join_code:
      return render_template("home.html", error_message="Please enter a join code", join_code=join_code,name=name)

    room = join_code
    if create!= False : # that means Create room button is clicked
      # Generate random join code for new room
        room = generate_room_code(7) # generate 7 char random string using defined function
        rooms[room] = {"members":0, "users": [], "messages": [], "media": []}
      
    elif join_code not in rooms:
      return render_template("home.html", error_message="Room code not found", join_code=join_code,name=name)
    session['join_code'] = join_code
    session['name'] = name
    session['room'] = room
    
    # Mongodb DATABASE
    database = mongo.db[room]
    date = datetime.now()
    database.insert_one({"created_by_name":name,"join_code":room,"date":date})
    
    return redirect(url_for('room'))
    
  return render_template("home.html")


@app.route('/room')
def room():
  room = session.get('room')
  if room is None or session.get('name') is None or room not in rooms:
    return redirect(url_for('home'))
  
  return render_template('room.html',room=room, messages=rooms[room]['messages'])


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    
    send(content, to=room)
    rooms[room]["messages"].append(content)
    
    # Database Added
    database = mongo.db[room]
    date = datetime.now()
    database.insert_one({"member":session.get("name"),"message":data["data"], "date":date})
    
    print(f"{session.get('name')} said: {data['data']}")
    
@socketio.on("file")
def myFile(media):
    room = session.get("room")
    if room not in rooms:
        return 
    
    image = media["media"] # <- {'name': 'Uzumaki', 'file': {}} 
    image_base64 = base64.b64encode(image).decode('utf-8')
    
    content = {
        "name": session.get("name"),
        "file": image_base64
    }
    # print(content)
    send(content, to=room)
    rooms[room]["media"].append(content)
    
    # Database Added
    database = mongo.db[room]
    date = datetime.now()
    database.insert_one({"member":session.get("name"),"file":image_base64, "date":date})
    
    # print(f"{session.get('name')} said: {media['media']}")

@socketio.on('connect')
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=5000, host='0.0.0.0')

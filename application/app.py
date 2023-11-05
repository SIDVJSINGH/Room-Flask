from flask import Flask, render_template, url_for, request, session, redirect
from flask_socketio import SocketIO, emit, leave_room, send, join_room
import random
from string import ascii_lowercase, digits,ascii_uppercase
from datetime import timedelta

app = Flask(__name__)
# app.config['SECRET_KEY'] = ''.join(random.choice(ascii_lowercase + digits + ascii_uppercase) for i in range(16))
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {} # {"room_code": {"members":0, "users": [], "messages": []}}

def generate_room_code(length:int):
  while True:
    room_code = ""
    for _ in range(length):
      room_code += random.choice(ascii_lowercase + digits + ascii_uppercase)
    if room_code not in rooms: # if the room_code exist in rooms dict, generate new one
      break
  return room_code

@app.route('/', methods=['GET', 'POST'])
def home():  
  session.clear()
  
  if request.method == 'POST':
    # Session Timeout in 30 seconds
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=30)
     
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
        # room = ''.join(random.choice(ascii_lowercase + digits + ascii_uppercase) for i in range(6)) # generate 6 char random string Lambda function
        room = generate_room_code(8) # generate 8 char random string using defined function
        rooms[room] = {"members":0, "users": [], "messages": []}
      
    elif join_code not in rooms:
      return render_template("home.html", error_message="Room code not found", join_code=join_code,name=name)
    session['join_code'] = join_code
    session['name'] = name
    session['room'] = room
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
    print(f"{session.get('name')} said: {data['data']}")

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
    socketio.run(app, debug=True,allow_unsafe_werkzeug=True, port=5000, host='0.0.0.0')
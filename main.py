# create a flask minimal template


from flask import Flask, redirect, render_template,request,session
import json
import random
app = Flask(__name__)
# declare the session
app.secret_key = 'my precious'
@app.route('/')
def index():
    return render_template('index.html')

# create a function that controls the action of submit button in the form and the route will be /room
# this function will extract the content of a input whose name is room_name


@app.route('/room',methods=['GET','POST'])
def room():
    if request.method == 'POST':
        # get the content of the input whose name is room_name
        room_name = request.form['room_name']
        password = request.form['password']
        user_name = request.form['username']
        user_pass = request.form['userPassword']
        with open('templates/content.json', 'r') as f:
            previousRooms = json.loads(f.read())
        if room_name in previousRooms['rooms'].keys():
            if password == previousRooms['rooms'][room_name][1]:
                # open users.json as read the content
                with open('templates/users.json', 'r') as f:
                    users = json.loads(f.read())
                for i,j in users.items():
                    if user_name == i:
                        if user_pass == j:
                            chats = previousRooms['rooms'][room_name][2]
                            session['random'] = str(random.randint(1,100000))
                            previousRooms['rooms'][room_name][2].append(user_name+" just entered.. say hi!👋")
                            with open("content.json", 'w') as d:
                                d.write(json.dumps(previousRooms))
                            return render_template('chats.html', room_name=room_name, chats=chats,username=user_name)
                        else:
                            return "<h1>Wrong User Password! Try again...</h1>"
                else:
                    # enter the user_name and user_password in users.json
                    users[user_name] = user_pass
                    with open('templates/users.json', 'w') as f:
                        json.dump(users, f)
                    return "<h1>New Account Created!</h1>"

                
            else:
                return "<h1>Wrong Room Password, Try again</h1>"
        else:
            # write the room_name in the json file of content.json
            previousRooms['rooms'][room_name] = []
            previousRooms['rooms'][room_name].append("".join([str(random.randint(0,9)) for _ in range(20)]))
            previousRooms['rooms'][room_name].append(password)
            previousRooms['rooms'][room_name].append([])
            
            with open('templates/content.json', 'w') as f:
                f.write(json.dumps(previousRooms))
            return render_template('room.html', room_name=room_name)
@app.route(f"/chatting",methods=['GET','POST'])
def chatting():
    if request.method == 'POST':
        username = request.form['username']
        room_name = request.form['room_name']
        with open('templates/content.json', 'r') as f:
            previousRooms = json.loads(f.read())
        if username + "<>:<> " + request.form['NewChat'] not in previousRooms['rooms'][room_name][2]:
            previousRooms['rooms'][room_name][2].append(username + "<>:<> " + request.form['NewChat'])
        # write the previousRooms in content.json
        with open('templates/content.json', 'w') as f:
            f.write(json.dumps(previousRooms))
        session['random'] = str(random.randint(1,100000))
        return render_template('chats.html', room_name=room_name, chats=previousRooms['rooms'][room_name][2],username=username)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

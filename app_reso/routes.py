from flask import Blueprint,  render_template, request, redirect, url_for, flash, session, json
from app_reso import db
from app_reso.database import Users
import bcrypt

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['POST', 'GET'])
def home():
    """
    login template for users to login in to their account
    """
    if request.method == 'POST':  # if user submits a login check if it exists
        username = request.form.get('username')
        password = request.form.get('password')

        users = Users.query.filter_by(
            username=username).first()  # get all the usernames that are in DB that match with entered username

        # enocode both since we encoded when storing in db. will compare bytes
        if users and bcrypt.checkpw(password.encode('utf-8'), users.password.encode(
                'utf-8')):  # password: user input, users.password: hashed password stored in DB
            session['username'] = username
            print("sessions ", session['username'])
            return redirect('/room')
        else:
            flash('Username or password are incorrect')
            return render_template('login.html', error="alert")
    else:
        if 'username' in session:  # user is still signed in, no need to re-sign in
            return redirect('/room')
        return render_template('login.html')



@routes.route('/signup', methods=['POST', 'GET'])
def signup():
    """
    signup template where users create their account
    """
    if request.method == 'POST':  # if user submits a login credential to signup then store it in DB
        username = request.form['username']
        password = request.form['password']

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # hash the user password

        new_user = Users(username=username, password=hashed)  # Create Users object to store the credentials

        try:
            db.session.add(new_user)  # send it to the DB
            db.session.commit()
            return redirect('/')
        except Exception as e:  # the entered credentials already exist so tell them and redirect to error.html
            print(e)
            flash("User already exists. Try another username")
            return render_template('signup.html')
    else:
        return render_template('signup.html')


@routes.route('/logout')
def logout():
    """
    logout template when user clicks logout
    """
    flash('You have been logged out.')
    session.pop('username', None)  # log out the user
    return render_template('login.html')


@routes.route('/chat', methods=['POST', 'GET'])
def chat():
    """
    chatting template if already logged in or if successfully logged in after entering room
    """
    if 'username' not in session:
        return redirect(url_for('routes'))
    else:
        defaultroom = request.form['room']
        session['room'] = defaultroom
        if request.method == "POST":
            return render_template('chat.html')
        return render_template('chat.html', userroom = defaultroom)


@routes.route('/room', methods=['GET', 'POST'])
def room():
    """
    room template where user choose their room to join
    """
    if 'username' not in session:
        return redirect(url_for(''))
    else:
        if request.method == "POST":
            return render_template('room.html', chat=True)
        return render_template('room.html', chat=True)

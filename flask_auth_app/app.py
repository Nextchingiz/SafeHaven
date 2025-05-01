# app.py
from flask import Flask, render_template, request, redirect, session, url_for, flash
import json
import os
from datetime import datetime
HISTORY_FOLDER = os.path.join(os.path.dirname(__file__), 'history')
USER_DATA_FILE = "user_data.json"
USERS_FOLDER = os.path.join(os.path.dirname(__file__), 'users')
if not os.path.exists(USERS_FOLDER):
    os.makedirs(USERS_FOLDER)


app = Flask(__name__)
app.secret_key = 'safehaven'

# keeps users in a "database"
class Account:
    def __init__(self, username: str, password: str, number: str):
        self.username = username
        self.password = password
        self.number = number

    @staticmethod
    def from_dict(data):
        return Account(data['username'], data['password'], data['number'])
    
    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'number': self.number
        }
    
    @staticmethod
    def load_user(username):
        user_file = os.path.join(USERS_FOLDER, f"{username}.json")
        if not os.path.exists(user_file):
            return None  # User not found

        with open(user_file, 'r') as f:
            data = json.load(f)
            return Account.from_dict(data)
    
    @staticmethod
    def save_user(account):
        user_file = os.path.join(USERS_FOLDER, f"{account.username}.json")
        with open(user_file, 'w') as f:
            json.dump(account.to_dict(), f, indent=4)
    
    @staticmethod
    def load_all_users():
        users = {}
        for filename in os.listdir(USERS_FOLDER):
            if filename.endswith('.json'):
                username = filename.replace('.json', '')
                user_file = os.path.join(USERS_FOLDER, filename)
                with open(user_file, 'r') as f:
                    data = json.load(f)
                    users[username] = Account.from_dict(data)
        return users


# stores user data as username for the key and the account class is the value
users = Account.load_all_users()

# Function to get all detection history for a specific user
def get_user_detections(username):
    history_file = os.path.join(HISTORY_FOLDER, f"{username}_history.json")
    
    if not os.path.exists(history_file):
        return []
    
    with open(history_file, 'r') as f:
        data = json.load(f)
        return data['detections']

# route to direct the user to home page if they were logged in
@app.route('/')
def home():
    if 'username' in session:  # checks if user is logged in
        user = users.get(session['username'])
        if user:
            return render_template('home.html', username=user.username)
        else:
            flash("Welcome To SafeHaven, Please Login")
            session.pop('username', None)
            return redirect(url_for('login'))
    return redirect(url_for('login'))



# route that directs them to sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        number = request.form['number']
        password = request.form['password']

        if username in users:
            flash('Username already exists. Please choose another one.')
            return redirect(url_for('signup'))

        # creates and saves new account
        new_account = Account(username, password, number)
        Account.save_user(new_account) # save user to seperate file
        users[username] = new_account # add to in memory dictionary
        flash('Account Created! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')



# route that directs them to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        account = Account.load_user(username)
        if account and account.password == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

# redirects them home if they logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("you have been logged out")
    return redirect(url_for('login'))

@app.route('/settings')
def settings():
    if 'username' in session:
        user = users.get(session['username'])
        if user:
            return render_template(
                'settings.html',
                username=user.username,
                number=user.number
            )
        else:
            flash("User not found. Please log in again.")
            session.pop('username', None)
            return redirect(url_for('login'))
    else:
        flash("You need to log in first.")
        return redirect(url_for('login'))

@app.route('/history')
def history():
    if 'username' not in session:
        flash("Please log in to view history")
        return redirect(url_for('login'))
    
    username = session['username']
    detections = get_user_detections(username)
    
    # Sort detections by timestamp (newest first)
    detections.sort(key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    
    return render_template('history.html', detections=detections)

if __name__ == '__main__':
    app.run(debug=True)

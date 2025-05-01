# app.py
from flask import Flask, render_template, request, redirect, session, url_for, flash
import json
import os
from datetime import datetime
from SafeHaven import HISTORY_FOLDER  # Import from your main program

app = Flask(__name__)
app.secret_key = 'safehaven'

# keeps users in a "database"
class Account:
    def __init__(self, username: str, password: str, email: str, number: str):
        self.username = username
        self.password = password
        self.email = email
        self.number = number

# stores user data as username for the key and the account class is the value
users = {}

# Function to get all detection history for a specific user
def get_user_detections(username):
    history_file = os.path.join(HISTORY_FOLDER, f"{username}_history.json")
    
    if not os.path.exists(history_file):
        return []
    
    with open(history_file, 'r') as f:
        data = json.load(f)
        return data['detections']
    
# Check user updates
def is_recent(timestamp_str):
    """Returns True if timestamp is within the last 5 minutes."""
    detection_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return (datetime.now() - detection_time).total_seconds() < 300  # 300 seconds = 5 minutes, Check every 5 minutes

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
        password = request.form['password']
        phone = request.form['number']  # Only username/password/phone now

        # Load existing data
        try:
            with open('user_data.json', 'r') as f:
                user_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            user_data = {}

        if username in user_data:
            flash('Username already exists!')
            return redirect(url_for('signup'))

        # Save only these 3 fields
        user_data[username] = {
            "password": password,
            "phone": phone  # No more email
        }

        with open('user_data.json', 'w') as f:
            json.dump(user_data, f, indent=4)

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('signup.html')

# route that directs them to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            with open('user_data.json', 'r') as f:
                user_data = json.load(f)
        except:
            flash('System error: No user data found')
            return redirect(url_for('login'))

        # Strict check (case-sensitive)
        if username in user_data and user_data[username]['password'] == password:
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
                email=user.email,
                number=user.number
            )
        else:
            flash("User not found. Please log in again.")
            session.pop('username', None)
            return redirect(url_for('login'))
    else:
        flash("You need to log in first.")
        return redirect(url_for('login'))

# Redirects tp the history page
@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    history_file = os.path.join('Users_History', f'{username}_history.json')
    
    # Load detection history or create empty list if file doesn't exist
    try:
        with open(history_file, 'r') as f:
            detections = json.load(f).get('detections', [])
    except (FileNotFoundError, json.JSONDecodeError):
        detections = []
    
    # Sort by timestamp (newest first) and add 'is_recent' flag
    detections.sort(key=lambda x: x['timestamp'], reverse=True)
    for detection in detections:
        detection['is_recent'] = is_recent(detection['timestamp'])
    
    return render_template('history.html', detections=detections)

if __name__ == '__main__':
    app.run(debug=True)
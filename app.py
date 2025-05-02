# Libraries we will need for this flask web server
from flask import Flask, render_template, request, redirect, session, url_for, flash # Different functions we need for the web app to function
import json # json files to be accessed for info
import os # Same, json files thing
from datetime import datetime # Time
from SafeHaven import HISTORY_FOLDER  # Import from the main program the history folder variable

# Define the app
app = Flask(__name__)
app.secret_key = 'safehaven'

# keeps users in a "database type of system", we will create a class for it
class Account:
    def __init__(self, username: str, password: str, email: str, number: str):
        self.username = username
        self.password = password
        self.email = email
        self.number = number
        # Pretty self explanatory here

# stores user data as username for the key and the account class is the value
users = {}

# Function to get all detection history for a specific user
def get_user_detections(username):
    history_file = os.path.join(HISTORY_FOLDER, f"{username}_history.json")
    
    # Whatif it is not there? (The history file for the specific username)
    if not os.path.exists(history_file):
        return []
    
    # Open and load the file if it is actually there
    with open(history_file, 'r') as f:
        data = json.load(f)
        return data['detections']
    
# Check user updates each 5 minutes for example
def is_recent(timestamp_str):
    """Returns True if timestamp is within the last 5 minutes."""
    detection_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return (datetime.now() - detection_time).total_seconds() < 300  # 300 seconds = 5 minutes, Check every 5 minutes

# Route to direct the user to home page if they were logged in
@app.route('/')
def home():
    if 'username' in session:  # checks if user is logged in successfully
        user = users.get(session['username'])
        if user:
            return render_template('home.html', username = user.username)
        else:
            flash("Welcome To SafeHaven, Please Login")
            session.pop('username', None)
            return redirect(url_for('login'))
    return redirect(url_for('login')) # Redirect them

# Route that directs them to sign up
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'] # Request all this info
        password = request.form['password']
        phone = request.form['number']  # Only username/password/phone now, because the email was not functional

        # Load the existing data from the json file
        try:
            with open('user_data.json', 'r') as f:
                user_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            user_data = {}

        # Check if there is someone already using the username prompted
        if username in user_data:
            flash('Username already exists!')
            return redirect(url_for('signup'))

        # Save only these 3 fields, because we got rid of the email lately
        user_data[username] = {
            "password": password,
            "phone": phone  # No more email
        }

        # Just store the information we got, the same way a in SafeHaven.py
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f, indent = 4)

        # Message telling that the registration was successful
        flash('Registration successful!')
        return redirect(url_for('login')) # Redirect to the login

    # Render/start/open/load template of the sign up page (stored in the templates folder)
    return render_template('signup.html')

# Route that directs the users to the to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip() # Ask for info
        password = request.form.get('password', '').strip()
        
        # Load the user_data.json file
        try:
            with open('user_data.json', 'r') as f:
                user_data = json.load(f)
        except:
            flash('System error') # if not, go back to the login page
            return render_template('login.html')

        # Check if the user is in our "database" and the username and password are the same
        if username in user_data and user_data[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))  # Go to the home page
        
        # If not, we will tell the user there was an error
        flash('Invalid username or password')
    
    # For GET requests or failed logins
    return render_template('login.html') # Just changed this, my bad, I put thew wrong html file

# Redirects to the home page
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("you have been logged out") # Tell what is going on
    return redirect(url_for('login')) # Redirect to the original login page

# Redirects to the settings page
@app.route('/settings')
def settings():
    if 'username' in session:
        user = users.get(session['username']) # Make use of the current username to display it
        if user:
            return render_template(
                'settings.html',
                username = user.username,
                email = user.email,
                number = user.number
                # Put the necessary variables our template requires
            )
        else:
            flash("User not found. Please log in again.") 
            session.pop('username', None)
            return redirect(url_for('login'))
    else:
        flash("You need to log in first.") # What if someone somehow accesses the page without logging in
        return redirect(url_for('login'))

# Redirects to the history page
@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Use the current username, to access its specific history file
    username = session['username']
    history_file = os.path.join('Users_History', f'{username}_history.json')
    
    # Load detection history or create an empty list if the file doesn't exist yet
    try:
        with open(history_file, 'r') as f:
            detections = json.load(f).get('detections', [])
    except (FileNotFoundError, json.JSONDecodeError):
        detections = []
    
    # Sort by timestamp (newest first)
    detections.sort(key=lambda x: x['timestamp'], reverse = True)
    for detection in detections:
        detection['is_recent'] = is_recent(detection['timestamp'])
    
    # Render the history template we got in the templates file
    return render_template('history.html', detections=detections)

# Start the program
if __name__ == '__main__':
    app.run(debug = True)
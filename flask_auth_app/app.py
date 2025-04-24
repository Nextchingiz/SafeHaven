from flask import Flask, render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key = 'safehaven'

# keeps users in a "database"
class Account:

    def __init__(self, username:str, password: str, email:str, number: str):
        self.username = username
        self.password = password
        self.email = email
        self.number = number
# stores user data as username for the key and the accoun class is the value
users = {}

# route to direct the user to home page if they were logged in
@app.route('/')
def home():
    if 'username' in session: # checks if user is logged in
        user = users.get(session['username'])

        if user:
            return render_template('home.html', username=user.username, password = user.password, email = user.email, number = user.number)
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
        email = request.form['email']    # collect email and phone number to store in the Account Class
        number = request.form['number']
        password = request.form['password']

        # checks if username exist
        if username in users:
            flash('Username already exists. Please choose another one.')
            return redirect(url_for('signup'))

        users[username] = Account(username, password, email, number)  # Store user # CHANGED: now stores password, phone number, email
        flash('Account Created! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')


# route that directs them to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        account = users.get(username)
        if account and account.password == password: # change this so it checks the users account, not just the string
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

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' in session: 
        user = users.get(session['username']) # grabs users account object from "database"
        if user:
            return render_template(
                'settings.html',
                username=user.username,
                email=user.email,
                number=user.number
            )
        else:
            flash("User not found. Please log in again.")
            session.pop('username', None) # logs them out
            return redirect(url_for('login'))
    else:
        flash("You need to log in first.") # if their username isn't in the session tell them to login
        return redirect(url_for('login'))

@app.route('/history', methods=['GET', 'POST'])
def history():
    pass


def generate_html_log():
    with open("detection_log.txt", "r") as log_file: # opens file and reads it
        log_lines = log_file.readlines() # stores all lines from the text file into a list
    

     # Read the existing HTML file
    with open("history.html", "r") as html_file:
        html_content = html_file.read()

    # Generate list items from logs
    list_items = "\n".join(f"<li>{line.strip()}</li>" for line in log_lines) # goes through each line in the list from earlier and makes a list of strings


    # Insert the log into the HTML using a marker (div with id="log")
    updated_html = html_content.replace(
        '<div id="log">', f'<div id="log">\n<ul>\n{list_items}\n</ul>'
    )

    # Write the updated HTML back
    with open("history.html", "w") as html_file:
        html_file.write(updated_html)

    return render_template('history.html', contents=log_lines)
if __name__ == '__main__':
    app.run(debug=True)

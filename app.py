from flask import Flask, render_template ,request, redirect, url_for, session
import sqlite3

x = sqlite3.connect('messages.db')
cursor = x.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        message TEXT NOT NULL
                    )''')
x.commit()
x.close()



app = Flask(__name__)
app.secret_key = 'iouhfekljhfewsf5645415%^$%^#'

# home route
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html')

# about route
@app.route('/about')
def about():
    return render_template('about.html')


# contact route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        n = request.form["name"]
        e = request.form["email"]
        m = request.form["message"]
        x = sqlite3.connect('messages.db')
        cursor = x.cursor()
        cursor.execute(f"INSERT INTO messages (name, email, message) VALUES ('{n}', '{e}', '{m}')")
        x.commit()
        x.close()

        return render_template("thank_you.html", name=n)
    return render_template("contact.html")

# messages route
@app.route('/messages')
def messages():
    x = sqlite3.connect('messages.db')
    cursor = x.cursor()

    cursor.execute('SELECT * FROM messages')
    m = cursor.fetchall()
    x.close()

    return render_template('messages.html', messages = m)

# delete all messages route
@app.route('/delete_all', methods=['POST'])
def delete_all():
    x = sqlite3.connect('messages.db')
    cursor = x.cursor()

    cursor.execute('DELETE FROM messages')
    x.commit()
    x.close()
    return redirect(url_for('messages'))


# delete one message
@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    x = sqlite3.connect('messages.db')
    cursor = x.cursor()
    cursor.execute(f'DELETE FROM messages WHERE id = {message_id}')
    x.commit()
    x.close()

    x = sqlite3.connect('messages.db')
    cursor = x.cursor()
    cursor.execute('SELECT * FROM messages')
    m = cursor.fetchall()

    return redirect(url_for('messages'))


# creating table for users
x = sqlite3.connect('messages.db')
cursor = x.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               email TEXT NOT NULL UNIQUE,
               password TEXT NOT NULL
               )
""")
x.commit()
x.close()

# register new acount
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        n = request.form['username']
        e = request.form['email']
        p = request.form['password']

        x = sqlite3.connect('messages.db')
        cursor = x.cursor()
        cursor.execute(f"INSERT INTO users (username, email, password) VALUES ('{n}', '{e}', '{p}')")
        x.commit()
        x.close()
        return  redirect('/login')
    return render_template('register.html')

# login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        e = request.form['email']
        p = request.form['password']

        x = sqlite3.connect('messages.db')
        cursor = x.cursor()
        cursor.execute(f'SELECT * FROM users WHERE email = "{e}" AND password = "{p}"')
        user = cursor.fetchone()

        if user != []:
            session['user_id'] = user[0]
            return redirect('/')
        else:
            return "Invalid Email or Password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    x = sqlite3.connect('messages.db')
    cursor = x.cursor()
    cursor.execute(f'SELECT * FROM users WHERE id = {session["user_id"]}')
    user = cursor.fetchone()
    
    x.close()

    if user:
        return render_template('profile.html', u_name = user[1])


if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'intro'  # Replace with a secure secret key

# Dummy user data for login validation
users = {
    'yoga': '222',
    'gokul': '444'
}

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('self_intro'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/self_intro')
def self_intro():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Example self introduction and responsibilities
    intro = "Hello, I am " + session['username'] + "."
    responsibilities = [
        "Manage projects",
        "Write code",
        "Review pull requests",
        "Collaborate with team"
    ]
    return render_template('self_intro.html', intro=intro, responsibilities=responsibilities)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)

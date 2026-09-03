from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import init_db, add_message, get_all_messages, delete_message

app = Flask(__name__, template_folder='template', static_folder='static')

# A secret key is required for flash messages AND for login sessions to work
# (Flask uses it to cryptographically sign the session cookie so it can't be
# tampered with). For a school project this can just be any string, but in
# a real app it should be kept secret / loaded from an environment variable.
app.secret_key = 'dev-secret-key-change-this'

# The password needed to view /messages. In a real app this would never be
# a plain string in the source code -- it'd be hashed and stored in the
# database, or loaded from an environment variable. For an MVP/assessment,
# a hard-coded constant is fine, but it's worth naming this as a known
# limitation in your documentation.
ADMIN_PASSWORD = 'changeme123'

# Make sure the messages table exists before the app starts handling requests.
init_db()


def login_required(view_function):
    """
    A decorator that protects a route so it can only be accessed after
    logging in. Any route wrapped with @login_required will redirect to
    the login page if session['logged_in'] hasn't been set to True.

    Wrapping this around a route instead of copy-pasting the same check
    into every function means the login logic only has to be written once.
    """
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view_function(*args, **kwargs)
    return wrapper


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/research')
def research():
    return render_template('research.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('message')

        # Basic server-side validation. The HTML 'required' attribute
        # stops most empty submissions, but that only runs in the browser
        # -- a request sent directly (e.g. via a script) could skip it,
        # so we check again here on the server.
        if not email or not message:
            flash("Please fill in both your email and a message.", "error")
            return redirect(url_for('contact'))

        add_message(email, message)
        flash("Thanks! Your message has been sent.", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')

        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash("Logged in successfully.", "success")
            return redirect(url_for('messages'))
        else:
            flash("Incorrect password.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You've been logged out.", "success")
    return redirect(url_for('login'))


@app.route('/messages')
@login_required
def messages():
    all_messages = get_all_messages()
    return render_template('messages.html', messages=all_messages)


@app.route('/messages/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message_route(message_id):
    # methods=['POST'] means this can only be triggered by a form submission,
    # not by just visiting a URL -- stops someone accidentally (or
    # maliciously) deleting messages just by clicking a link or a browser
    # pre-fetching a URL. @login_required also means you have to be logged
    # in to delete anything, same as viewing the page.
    delete_message(message_id)
    flash("Message deleted.", "success")
    return redirect(url_for('messages'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, redirect, render_template request, redirect, url_for, flash
from database import init_db, add_message, get_all_messages
 

app = Flask(__name__, template_folder='template', static_folder='static')

app.secret_key = 'dev-secret-key-change-this'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('message')


  flash("Please fill in both your email and a message.", "error")
            return redirect(url_for('contact'))


 add_message(email, message)
        flash("Thanks! Your message has been sent.", "success")
        return redirect(url_for('contact'))

     return render_template('contact.html') 

@app.route('/messages')
def messages():
    all_messages = get_all_messages()
    return render_template('messages.html', messages=all_messages)


if __name__ == '__main__':
    app.run(debug=True) 
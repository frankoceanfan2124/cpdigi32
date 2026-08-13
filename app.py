from flask import Flask, render_template

#  Flask applciatiion
# make sure it matches my folder structure
app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/')
def home():
    # this is the thingy for index
    return render_template('index.html')


if __name__ == '__main__':
   
    app.run(debug=True)

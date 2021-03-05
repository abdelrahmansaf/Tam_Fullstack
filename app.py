from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def entry_point():
    return render_template('./app.html')

@app.route('/hello_world')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template
import os

app = Flask(__name__, static_url_path='', static_folder='public')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/picker')
def picker():
    return app.send_static_file('picker.html')

if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', True),
            port=int(os.environ.get('PORT', 5000)))

from flask import Flask
from blueprints.match_routes import match_blueprint

app = Flask(__name__)
app.register_blueprint(match_blueprint)
if __name__ == '__main__':
    app.run(debug=True)

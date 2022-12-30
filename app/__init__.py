from flask import Flask, render_template
from flask_cors import CORS
from app.mod_auth.controllers import mod as pages_module
from app.module_one.controllers import mod as alert_module

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
	return render_template("index.html")

app.register_blueprint(pages_module)
app.register_blueprint(alert_module)
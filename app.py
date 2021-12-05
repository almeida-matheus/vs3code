from flask import Flask
from base_app.view import base_view
from base_app.resources.filters import file_type
from base_app.resources.filters import datetime_format

app = Flask(__name__)
app.secret_key = 'secret'
app.register_blueprint(base_view)
app.jinja_env.filters['file_type'] = file_type
app.jinja_env.filters['datetime_format'] = datetime_format

if __name__ == "__main__":
    app.run(debug=True, port=8001)
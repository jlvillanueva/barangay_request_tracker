
from flask import Flask
from flask_restful import Api
from mobile_sql_alchemy import mobile_db
from config import DefaultConfig

app = Flask(__name__)
app.config.from_object(DefaultConfig)
mobile_db.init_app(app)
api = Api(app)


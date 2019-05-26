from flask import Flask
import pymysql
from flask_cors import *

pymysql.install_as_MySQLdb()
from .controller import *
from flask_sqlalchemy import SQLAlchemy

# 创建项目对象
app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/qms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)




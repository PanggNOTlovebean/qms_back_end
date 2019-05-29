from flask_restful import Resource, reqparse, abort
from qms import db
from ..model.models import *

parser = reqparse.RequestParser()

parser.add_argument("username")
parser.add_argument("password")
parser.add_argument("type")
class LoginCheck(Resource):
    def post(self):
        args=parser.parse_args()
        username=args.get("username")
        password=args.get("password")
        print(username)
        print(password)
        ret_data={}
        Session=db.session
        user=Session.query(User).filter(User.username==username,User.password==password).first()
        if user:
            ret_data['auth']=user.authority
            print(ret_data)
            return ret_data,200
        return "找不到用户",403
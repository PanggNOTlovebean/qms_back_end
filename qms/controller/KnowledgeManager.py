from flask_restful import Resource, reqparse, abort
from qms import db
from ..model.models import *

parser = reqparse.RequestParser()

parser.add_argument("school_id")
parser.add_argument("name")
parser.add_argument("type")


class QueryAllKnowledge(Resource):
    def get(self):
        Session=db.session
        schools=Session.query(School).all()
        ret_data=[]
        for school in schools:
            ret_item={}
            ret_item['school_id']=school.id
            ret_item['type']=school.type
            ret_item['name']=school.name
            ret_data.append(ret_item)
        Session.close()
        return ret_data,200

class UpdateKnowledge(Resource):
    def post(self):
        args = parser.parse_args()
        school_id=args.get("school_id")
        name=args.get("name")
        type=args.get("type")
        Session=db.session
        Session.query(School).filter(School.id==school_id).update({'name':name,'type':type})
        Session.commit()
        Session.close()
        return "success",200

class DeleteKnowledge(Resource):
    def post(self):
        args = parser.parse_args()
        school_id = args.get("school_id")
        Session=db.session
        ret=Session.query(School).filter(School.id == school_id).delete()
        Session.commit()
        Session.close()
        if ret==0:
            return "not found",404
        return "success",200


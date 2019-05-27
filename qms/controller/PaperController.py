from flask_restful import Resource, reqparse, abort
from qms import db
from ..model.models import *
from qms.common.gen import get_uuid
parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("school")
parser.add_argument("subject")
parser.add_argument("grade")
parser.add_argument("score")
parser.add_argument("singlechoose",location='json')
parser.add_argument("multiplechoose")
parser.add_argument("judge")
parser.add_argument("blank")
parser.add_argument("discuss")
class addPaper(Resource):
    def post(selfs):
        args = parser.parse_args()
        name=args.get("name")
        schoolName=args.get("school")
        subject=args.get("subject")
        grade=args.get("grade")
        score=args.get("score")
        singlechoose=eval(args.get("singlechoose"))
        multiplechoose=eval(args.get("multiplechoose"))
        judge=eval(args.get("judge"))
        blank=eval(args.get("blank"))
        discuss=eval(args.get("discuss"))
        sum=singlechoose['num']+multiplechoose['num']+judge['num']+blank['num']+discuss['num']

        Session=db.session
        school=Session.query(School).filter_by(name=schoolName).first()
        pid=get_uuid()
        try:
            if not school:
                sid=get_uuid()
                Session.add(School(id=sid,name=schoolName))
                Session.commit()
            else:
                sid=school.id
            Session.add(Paper(id=get_uuid(),name=name,school=sid,subject=subject,grade=grade,score=score))

            Session.commit()
        except:
                return "数据库访问不知道出了啥错",500
        # except:
        #     print()
        #     return "failed",402
        res_data = {
            'singlechoose': [],
            'multiplechoose': [],
            'judge': [],
            'blank': [],
            'discuss': [],
            'paper_id':pid
        }
        for i in range(singlechoose['num']):
            res_data['singlechoose'].append(get_uuid())

        for i in range(multiplechoose['num']):
            res_data['multiplechoose'].append(get_uuid())

        for i in range(judge['num']):
            res_data['judge'].append(get_uuid())

        for i in range(blank['num']):
            res_data['blank'].append(get_uuid())

        for i in range(discuss['num']):
            res_data['discuss'].append(get_uuid())

        return res_data,200


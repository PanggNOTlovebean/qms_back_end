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

        print(name)
        print(schoolName)
        print(subject)
        print(grade)
        print(score)
        print(singlechoose)
        print(multiplechoose)
        print(judge)
        print(blank)
        print(discuss)

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
            Session.add(Paper(id=pid,name=name,school=sid,subject=subject,grade=grade,score=score))

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
        count=1
        for i in range(singlechoose['num']):
            qid=get_uuid()
            Session.add(QuestionInfo(id=qid,type="singlechoose",subject=subject,paper=pid,position=count,score=singlechoose['score']))
            res_data['singlechoose'].append(qid)
            count+=1

        for i in range(multiplechoose['num']):
            qid = get_uuid()
            Session.add(QuestionInfo(id=qid, type="multiplechoose", subject=subject, paper=pid, position=count,score=singlechoose['score']))
            res_data['multiplechoose'].append(qid)
            count += 1

        for i in range(judge['num']):
            qid = get_uuid()
            Session.add(QuestionInfo(id=qid, type="judge", subject=subject, paper=pid, position=count,score=singlechoose['score']))
            res_data['judge'].append(qid)
            count+=1

        for i in range(blank['num']):
            qid = get_uuid()
            Session.add(QuestionInfo(id=qid, type="blank", subject=subject, paper=pid, position=count,score=singlechoose['score']))
            res_data['blank'].append(qid)
            count += 1

        for i in range(discuss['num']):
            qid = get_uuid()
            Session.add(QuestionInfo(id=qid, type="discuss", subject=subject, paper=pid, position=count,score=singlechoose['score']))
            res_data['discuss'].append(qid)
            count += 1
        Session.commit()
        print(res_data)
        return res_data,200


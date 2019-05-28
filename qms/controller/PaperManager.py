from flask_restful import Resource, reqparse, abort
from qms import db
from ..model.models import *

parser = reqparse.RequestParser()

parser.add_argument("paper_id")
parser.add_argument("grade")
parser.add_argument("subject")
parser.add_argument("score")
parser.add_argument("name")

subject_dict={
    'chinese':'语文',
    'math':'数学',
    'english':'英语',
    'physical':'物理',
    'chemistry':'化学',
    'biology':'生物',
    'politics':'政治',
    'geography':'地理',
    'history':'历史',

}
class QueryAllPaper(Resource):
    def get(self):
        Session=db.session
        papers=Session.query(Paper).all()
        ret_data=[]
        for paper in papers:
            ret_item={}
            ret_item['paper_id']=paper.id
            ret_item['school_id']=paper.school
            ret_item['subject']=paper.subject
            ret_item['grade']=paper.grade
            ret_item['score']=paper.score
            ret_item['name']=paper.name
            ret_item['subject_ch'] = subject_dict[ret_item['subject']]
            school=paper.school1
            if school:
                ret_item['school_name'] = school.name
            ret_data.append(ret_item)
        Session.close()
        return ret_data,200

class UpdatePaper(Resource):
    def post(self):
        args = parser.parse_args()
        paper_id = args.get("paper_id")
        name = args.get("name")
        grade = args.get("grade")
        subject = args.get("subject")
        score = args.get("score")
        Session=db.session
        Session.query(Paper).filter(Paper.id==paper_id).update({'name':name,'grade':grade,'subject':subject,'score':score})
        questionInfos=Session.query(QuestionInfo).all()
        print(questionInfos)
        for questionInfo in questionInfos:
            if questionInfo.paper==int(paper_id):
                Session.query(QuestionInfo).filter(QuestionInfo.id==questionInfo.id).update({'subject':subject})
        Session.commit()
        Session.close()
        return "success",200

class DeletePaper(Resource):
    def post(self):
        args = parser.parse_args()
        paper_id = args.get("paper_id")
        Session=db.session
        ret=Session.query(Paper).filter(Paper.id == paper_id).delete()
        Session.commit()
        Session.close()
        if ret==0:
            return "not found",404
        return "success",200


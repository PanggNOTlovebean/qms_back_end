from flask_restful import Resource, reqparse, abort
from qms import db
from ..model.models import *
from qms.common.gen import get_uuid
import random

parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("school")
parser.add_argument("subject")
parser.add_argument("grade")
parser.add_argument("score")
parser.add_argument("singlechoose", location='json')
parser.add_argument("multiplechoose")
parser.add_argument("judge")
parser.add_argument("blank")
parser.add_argument("discuss")


def filterGrade(questionInfos, grade):
    rets = []
    # if not isinstance(questionInfos,list):
    #     rets.append(questionInfos)
    #     return rets
    for questionInfo in questionInfos:
        if questionInfo.paper1.grade == grade   :
            rets.append(questionInfo)
    return rets


class addPaper(Resource):
    def post(selfs):
        args = parser.parse_args()
        name = args.get("name")
        schoolName = args.get("school")
        subject = args.get("subject")
        grade = args.get("grade")
        score = args.get("score")
        singlechoose = eval(args.get("singlechoose"))
        multiplechoose = eval(args.get("multiplechoose"))
        judge = eval(args.get("judge"))
        blank = eval(args.get("blank"))
        discuss = eval(args.get("discuss"))

        Session = db.session
        school = Session.query(School).filter_by(name=schoolName).first()
        pid = get_uuid()
        try:
            if not school:
                sid = get_uuid()
                Session.add(School(id=sid, name=schoolName))
                Session.commit()
            else:
                sid = school.id
                p = Session.query(Paper).filter_by(name=name).first()
                if p:
                    return "已有同一试卷", 403
            Session.add(Paper(id=pid, name=name, school=sid, subject=subject, grade=grade, score=score))
            Session.commit()
        except Exception:
             return "数据库操作1错误", 500

        res_data = {
            'singlechoose': [],
            'multiplechoose': [],
            'judge': [],
            'blank': [],
            'discuss': [],
            'paper_id': pid
        }
        count = 1
        for i in range(singlechoose['num']):
            qid = get_uuid()
            Session.add(QuestionInfo(id=qid, type="singlechoose", subject=subject, paper=pid, position=count,
                                     score=singlechoose['score']))
            res_data['singlechoose'].append(qid)
            count += 1

        for i in range(multiplechoose['num']):
            qid = get_uuid()
            Session.add(QuestionInfo(id=qid, type="multiplechoose", subject=subject, paper=pid, position=count,
                                     score=singlechoose['score']))
            res_data['multiplechoose'].append(qid)
            count += 1

        for i in range(judge['num']):
            qid = get_uuid()
            Session.add(QuestionInfo(id=qid, type="judge", subject=subject, paper=pid, position=count,
                                     score=singlechoose['score']))
            res_data['judge'].append(qid)
            count += 1

        for i in range(blank['num']):
            qid = get_uuid()
            Session.add(QuestionInfo(id=qid, type="blank", subject=subject, paper=pid, position=count,
                                     score=singlechoose['score']))
            res_data['blank'].append(qid)
            count += 1

        for i in range(discuss['num']):
            qid = get_uuid()
            Session.add(QuestionInfo(id=qid, type="discuss", subject=subject, paper=pid, position=count,
                                     score=singlechoose['score']))
            res_data['discuss'].append(qid)
            count += 1
        Session.commit()
        print(res_data)
        return res_data, 200


class makePaper(Resource):
    def post(self):
        args = parser.parse_args()
        name = args.get("name")
        subject = args.get("subject")
        grade = int(args.get("grade"))

        singlechoose = eval(args.get("singlechoose"))
        multiplechoose = eval(args.get("multiplechoose"))
        judge = eval(args.get("judge"))
        blank = eval(args.get("blank"))
        discuss = eval(args.get("discuss"))

        Session = db.session

        res_data = {
            'singlechoose': [],
            'multiplechoose': [],
            'judge': [],
            'blank': [],
            'discuss': [],
        }

        questionInfos = Session.query(QuestionInfo).filter(QuestionInfo.subject == subject,
                                                           QuestionInfo.type == "singlechoose").all()
        questionInfos = filterGrade(questionInfos, grade)
        if len(questionInfos) < singlechoose['num']:

            return "题不够啦", 400
        # 生成要求数量的随机数

        random_list = random.sample(range(len(questionInfos)), singlechoose['num'])
        for i in random_list:
            questionDetail = Session.query(QuestionDetail).filter(
                QuestionDetail.question_info == questionInfos[i].id).first()
            res_data['singlechoose'].append(questionDetail.id)

        questionInfos = Session.query(QuestionInfo).filter(QuestionInfo.subject == subject,
                                                           QuestionInfo.type == "multiplechoose").all()
        questionInfos = filterGrade(questionInfos, grade)
        if len(questionInfos) < multiplechoose['num']:
            return "题不够啦", 400
        # 生成要求数量的随机数

        random_list = random.sample(range(len(questionInfos)), multiplechoose['num'])
        for i in random_list:
            questionDetail = Session.query(QuestionDetail).filter(
                QuestionDetail.question_info == questionInfos[i].id).first()
            res_data['multiplechoose'].append(questionDetail.id)

        questionInfos = Session.query(QuestionInfo).filter(QuestionInfo.subject == subject,

                                                           QuestionInfo.type == "judge").all()
        questionInfos = filterGrade(questionInfos, grade)
        if len(questionInfos) < judge['num']:
            return "题不够啦", 400
        # 生成要求数量的随机数

        random_list = random.sample(range(len(questionInfos)), judge['num'])
        for i in random_list:
            questionDetail = Session.query(QuestionDetail).filter(
                QuestionDetail.question_info == questionInfos[i].id).first()
            res_data['judge'].append(questionDetail.id)

        questionInfos = Session.query(QuestionInfo).filter(QuestionInfo.subject == subject,
                                                           QuestionInfo.type == "blank").all()
        questionInfos = filterGrade(questionInfos, grade)
        if len(questionInfos) < blank['num']:
            return "题不够啦", 400
        # 生成要求数量的随机数

        random_list = random.sample(range(len(questionInfos)), blank['num'])
        for i in random_list:
            questionDetail = Session.query(QuestionDetail).filter(
                QuestionDetail.question_info == questionInfos[i].id).first()
            res_data['blank'].append(questionDetail.id)

        questionInfos = Session.query(QuestionInfo).filter(QuestionInfo.subject == subject,
                                                           QuestionInfo.type == "discuss").all()
        questionInfos = filterGrade(questionInfos, grade)
        if len(questionInfos) < discuss['num']:
            return "题不够啦", 400
        # 生成要求数量的随机数

        random_list = random.sample(range(len(questionInfos)), discuss['num'])
        for i in random_list:
            questionDetail = Session.query(QuestionDetail).filter(
                QuestionDetail.question_info == questionInfos[i].id).first()
            res_data['discuss'].append(questionDetail.id)

        Session.commit()
        print(res_data)
        return res_data, 200

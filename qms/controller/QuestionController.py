from flask_restful import Resource, reqparse, abort
from qms import db
from ..model.models import *
import time
from qms.common.gen import get_uuid
import datetime

parser = reqparse.RequestParser()
# 问题信息parser
parser.add_argument("subject")
parser.add_argument("type")
parser.add_argument("hardness")
parser.add_argument("paper")
parser.add_argument("score")
parser.add_argument("position")
parser.add_argument("items", location='json')

# 问题详情parser
parser.add_argument("stem")
parser.add_argument("analysis")
parser.add_argument("answer")
parser.add_argument("info_id")


class addQuestionInfo(Resource):
    def get(self):
        return "success", 200

    def post(self):
        args = parser.parse_args()
        subject = args.get("subject")
        qtype = args.get("type")
        hardness = args.get("hardness")
        paper = args.get("paper")
        score = args.get("score")
        position = args.get("position")
        items = eval(args.get("items"))
        Session = db.session
        # 来源卷不存在 添加来源卷
        p = Session.query(Paper).filter_by(name=paper).first()
        if p:
            pid = p.id
        else:
            pid = get_uuid()
            print(pid)
            Session.add(Paper(id=pid, name=paper, subject=subject))
            Session.commit()
        knowledges_id = []
        # 知识点不存在 新增知识点
        for item in items:
            k = Session.query(Knowledge).filter_by(name=item["value"]).first()
            if k:
                knowledges_id.append(k.id)
            else:
                kid = get_uuid()
                Session.add(Knowledge(id=kid, name=item["value"]))
                knowledges_id.append(kid)
                Session.commit()
        qid = get_uuid()
        questionInfo = QuestionInfo(id=qid, type=qtype, subject=subject, hardness=hardness, paper=pid, score=score,
                                    position=position)
        for knowledge_id in knowledges_id:
            questionKnowledge = QuestionKnowledge(id=get_uuid(), question=qid, knowledge=knowledge_id)
            Session.add(questionKnowledge)
        Session.add(questionInfo)
        Session.commit()
        Session.close()
        # print(questionInfo)
        # 返回增加的id

        return {"id": qid}, 201


class addQuestionDetail(Resource):
    def post(self):
        args = parser.parse_args()
        stem = args.get("stem")
        answer = args.get("answer")
        info_id = args.get("info_id")
        analysis = args.get("analysis")
        print(stem)
        print(answer)
        print(info_id)
        print(analysis)
        Session = db.session
        if not Session.query(QuestionInfo).filter_by(id=info_id).first():
            return "找不到试题信息", 403
        else:
            questionDetail=QuestionDetail(id=get_uuid(),stem=stem,answer=answer,question_info=info_id,analysis=analysis)
            Session.add(questionDetail)
            Session.commit()
            Session.close()
        return "success", 201
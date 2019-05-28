from flask_restful import Resource, reqparse, abort
from qms import db
from ..model.models import *

type_dict = {
    'singlechoose': '单选题',
    'multiplechoose': '多选题',
    'blank': '填空题',
    'judge': '判断题',
    'discuss': '分析题'
}

subject_dict = {
    'chinese': '语文',
    'math': '数学',
    'english': '英语',
    'physical': '物理',
    'chemistry': '化学',
    'biology': '生物',
    'politics': '政治',
    'geography': '地理',
    'history': '历史',

}
parser = reqparse.RequestParser()
parser.add_argument("question_info_id", location='json')
parser.add_argument("question_detail_id")
parser.add_argument("hardness")
parser.add_argument("paper_id")
parser.add_argument("paper_name")
parser.add_argument("grade")
parser.add_argument("position")
parser.add_argument("score")
parser.add_argument("knowledges")
parser.add_argument("knowledges_id", location='json')


class QueryAllQuestion(Resource):
    def get(self):
        Session = db.session
        questionDetails = Session.query(QuestionDetail).all()
        ret_data = []
        for questionDetail in questionDetails:
            data_item = {}
            data_item['question_detail_id'] = questionDetail.id
            data_item['stem'] = questionDetail.stem
            data_item['answer'] = questionDetail.answer
            data_item['analysis'] = questionDetail.analysis
            data_item['question_info_id'] = questionDetail.question_info

            questionInfo = questionDetail.question_info1
            data_item['type'] = questionInfo.type
            data_item['subject'] = questionInfo.subject
            data_item['hardness'] = questionInfo.hardness
            data_item['paper_id'] = questionInfo.paper
            data_item['score'] = questionInfo.score
            data_item['position'] = questionInfo.position
            data_item['type_ch'] = type_dict[data_item['type']]
            data_item['subject_ch'] = subject_dict[data_item['subject']]

            paper = questionInfo.paper1
            data_item['paper_id'] = paper.id
            data_item['paper_name'] = paper.name
            data_item['school_id'] = paper.school
            data_item['grade'] = paper.grade
            data_item['paper_score'] = paper.score
            school = paper.school1
            if school:
                data_item['school_name'] = school.name
                data_item['school_type'] = school.type
            data_item['knowledges_id'] = []
            data_item['knowledges'] = ""
            knowledge_questions = Session.query(QuestionKnowledge).filter_by(question=questionInfo.id).all()
            knowledges = []

            for item in knowledge_questions:
                knowledges.append(item.knowledge1)

            for item in knowledges:
                data_item['knowledges_id'].append(item.id)
                data_item['knowledges'] += item.name + "|"
            data_item['knowledges'] = data_item['knowledges'][:-1]
            ret_data.append(data_item)
        Session.close()
        return ret_data, 200


class UpdateQuestion(Resource):
    def post(self):
        args = parser.parse_args()
        question_info_id = args.get("question_info_id")
        question_detail_id = args.get("question_detail_id")
        hardness = args.get("hardness")
        paper_id = args.get("paper_id")
        paper_name = args.get("paper_name")
        grade = args.get("grade")
        position = args.get("position")
        score = args.get("score")
        knowledges_id = eval(args.get("knowledges_id"))
        knowledges = args.get("knowledges")
        Session = db.session
        Session.query(QuestionInfo).filter(QuestionInfo.id == question_info_id).update(
            {"hardness": hardness, "position": position, "score": score})
        Session.query(Paper).filter(Paper.id == paper_id).update({"name": paper_name, "grade": grade})
        print(knowledges_id)
        print(knowledges)
        knowledges = knowledges.split('|')
        print(knowledges)
        if len(knowledges) != len(knowledges_id):
            return "知识点多了", 403
        for i in range(len(knowledges_id)):
            Session.query(Knowledge).filter(Knowledge.id == knowledges_id[i]).update({'name': knowledges[i]})
        Session.commit()
        Session.close()


class deleteQuestion(Resource):
    def post(self):
        args = parser.parse_args()

        info_id = args.get("question_info_id")

        Session = db.session
        ret = Session.query(QuestionInfo).filter(QuestionInfo.id == info_id).delete()

        Session.commit()
        Session.close()
        if ret == 0:
            return "not found", 404
        return "success", 200


class QueryOneQuestion(Resource):
    def post(self):
        Session = db.session()
        args = parser.parse_args()
        question_detail_id = args.get("question_detail_id")
        print(question_detail_id)
        question_detail = Session.query(QuestionDetail).filter(QuestionDetail.id == question_detail_id).first()
        ret_data = {}
        ret_data['stem'] = question_detail.stem
        ret_data['answer'] = question_detail.answer
        ret_data['analysis'] = question_detail.analysis
        Session.close()
        return ret_data, 200

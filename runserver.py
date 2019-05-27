from qms import app
from qms.controller.QuestionController import addQuestionInfo,addQuestionDetail
from qms.controller.PaperController import addPaper
from flask_restful import Api, Resource, reqparse, abort

api = Api(app)
api.add_resource(addQuestionInfo, '/addQuestionInfo', )
api.add_resource(addQuestionDetail, '/addQuestionDetail', )
api.add_resource(addPaper,'/addPaper')

if __name__ == '__main__':

    app.run(debug=True)
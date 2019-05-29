from qms import app
from qms.controller.QuestionController import addQuestionInfo,addQuestionDetail
from qms.controller.PaperController import addPaper,makePaper
from qms.controller.QuestionManager import QueryAllQuestion,UpdateQuestion,deleteQuestion,QueryOneQuestion
from qms.controller.SchoolManager import QueryAllSchool,UpdateSchool,DeleteSchool
from qms.controller.PaperManager import QueryAllPaper,UpdatePaper,DeletePaper
from qms.controller.KnowledgeManager import QueryAllKnowledge,UpdateKnowledge,DeleteKnowledge
from qms.controller.LoginController import LoginCheck

from flask_restful import Api, Resource, reqparse, abort

api = Api(app)
api.add_resource(addQuestionInfo, '/addQuestionInfo', )
api.add_resource(addQuestionDetail, '/addQuestionDetail', )
api.add_resource(addPaper,'/addPaper')
api.add_resource(makePaper,'/makePaper')
api.add_resource(QueryAllQuestion,'/getAllQuestion')
api.add_resource(UpdateQuestion,'/updateQuestion')
api.add_resource(deleteQuestion,'/deleteQuestion')
api.add_resource(QueryOneQuestion,'/getOneQuestion')

api.add_resource(QueryAllSchool,'/getAllSchool')
api.add_resource(UpdateSchool,'/updateSchool')
api.add_resource(DeleteSchool,'/deleteSchool')

api.add_resource(QueryAllPaper,'/getAllPaper')
api.add_resource(UpdatePaper,'/updatePaper')
api.add_resource(DeletePaper,'/deletePaper')
api.add_resource(LoginCheck,'/login')

api.add_resource(QueryAllKnowledge,'/getAllKnowledge')
api.add_resource(UpdateKnowledge,'/updateKnowledge')
api.add_resource(DeleteKnowledge,'/deleteKnowledge')


if __name__ == '__main__':

    app.run(debug=True)
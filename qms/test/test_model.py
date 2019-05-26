
from qms.model.models import User, Knowledge, School, Paper, QuestionInfo, QuestionDetail, QuestionKnowledge


def test_fun():
    user = User(id=1, username="admin", password="123456", authority=1)
    # session = db.session
    # session.add(user)
    # session.commit()



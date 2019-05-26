# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Knowledge(Base):
    __tablename__ = 'knowledge'

    id = Column(INTEGER(64), primary_key=True)
    name = Column(String(128))

    parents = relationship(
        'Knowledge',
        secondary='knowship',
        primaryjoin='Knowledge.id == knowship.c.father',
        secondaryjoin='Knowledge.id == knowship.c.son'
    )


class School(Base):
    __tablename__ = 'school'

    id = Column(INTEGER(64), primary_key=True)
    type = Column(String(128))
    name = Column(VARCHAR(128))


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(64), primary_key=True)
    username = Column(String(16), nullable=False)
    password = Column(String(16), nullable=False)
    authority = Column(String(16), nullable=False)


t_knowship = Table(
    'knowship', metadata,
    Column('father', ForeignKey('knowledge.id'), primary_key=True, nullable=False),
    Column('son', ForeignKey('knowledge.id'), primary_key=True, nullable=False, index=True)
)


class Paper(Base):
    __tablename__ = 'paper'

    id = Column(INTEGER(64), primary_key=True)
    name = Column(String(16))
    school = Column(ForeignKey('school.id'), index=True)
    subject = Column(String(16))
    grade = Column(INTEGER(8))
    score = Column(INTEGER(8))

    school1 = relationship('School')


class QuestionInfo(Base):
    __tablename__ = 'question_info'

    id = Column(INTEGER(64), primary_key=True)
    type = Column(String(16), nullable=False, index=True)
    subject = Column(String(16), nullable=False)
    hardness = Column(INTEGER(1), server_default=text("'0'"))
    paper = Column(ForeignKey('paper.id'), index=True)
    score = Column(INTEGER(16))
    position = Column(INTEGER(16))

    paper1 = relationship('Paper')


class QuestionDetail(Base):
    __tablename__ = 'question_detail'

    id = Column(INTEGER(64), primary_key=True)
    stem = Column(Text)
    answer = Column(Text)
    analysis = Column(Text)
    question_info = Column(ForeignKey('question_info.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    question_info1 = relationship('QuestionInfo')


class QuestionKnowledge(Base):
    __tablename__ = 'question_knowledge'

    id = Column(INTEGER(64), primary_key=True)
    question = Column(ForeignKey('question_info.id'), nullable=False, index=True)
    knowledge = Column(ForeignKey('knowledge.id'), nullable=False, index=True)

    knowledge1 = relationship('Knowledge')
    question_info = relationship('QuestionInfo')

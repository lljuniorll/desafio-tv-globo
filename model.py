import sqlalchemy as db
import constants as cons
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

# engine = db.create_engine('sqlite:///:memory:')
engine = db.create_engine('sqlite:///app.db')
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


class CutInstruction(Base):
    __tablename__ = cons.TABLE_CUT_INSTRUCTION
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(250), nullable=False)
    end_time = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    duration = db.Column(db.String(250), nullable=False)
    reconcile_key = db.Column(db.Integer, nullable=False)

    def __init__(self, start_time, end_time, title, duration, reconcile_key, id=None):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.title = title
        self.duration = duration
        self.reconcile_key = reconcile_key


class CutInstructionSchema(ModelSchema):
    class Meta:
        model = CutInstruction
        sqla_session = session


class CutJob(Base):
    __tablename__ = cons.TABLE_CUT_JOB
    id = db.Column(db.Integer, primary_key=True)
    job_external_id = db.Column(db.String(250), nullable=False)
    path = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(250), nullable=False, default=cons.STATUS_IN_PROGRESS)
    cut_instruction_id = db.Column(db.Integer, db.ForeignKey(f'{cons.TABLE_CUT_INSTRUCTION}.id'))
    cut_instruction = relationship("CutInstruction", backref=backref(cons.TABLE_CUT_JOB))

    def __init__(self, job_external_id, path, cut_instruction, id=None):
        self.id = id
        self.job_external_id = job_external_id
        self.path = path
        self.cut_instruction = cut_instruction


class CutJobSchema(ModelSchema):
    cut_instruction = fields.Nested(CutInstructionSchema, only=('id', 'title', 'duration'))

    class Meta:
        model = CutJob
        sqla_session = session


class CutFile(Base):
    __tablename__ = cons.TABLE_CUT_FILE
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(250), nullable=False)
    last_line = db.Column(db.Integer, nullable=False)
    filename_date = db.Column(db.String(8), nullable=False)
    filename_sequence = db.Column(db.Integer, nullable=False)

    def __init__(self, filename, last_line, filename_date, filename_sequence, id=None):
        self.id = id
        self.filename = filename
        self.last_line = last_line
        self.filename_date = filename_date
        self.filename_sequence = filename_sequence


class CutFileSchema(ModelSchema):
    class Meta:
        model = CutFile
        sqla_session = session


Base.metadata.create_all(engine)

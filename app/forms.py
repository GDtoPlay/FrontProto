from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from app.models import *
from app import db
from app.DatetimeCalc import InFiveMin
from app.IpParser import IpParser



class RegistrationForm(FlaskForm):
    flag_val = StringField('flag_Key_val', validators=[DataRequired()])
    flag_round = IntegerField('Round', validators=[DataRequired()])
    problem_id = IntegerField('Prob_id', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_flag_val(self, flag_val):
        Key = db.engine.execute("select * from flag_table where flag_val = '" + str(flag_val.data) + "'")
        if Key.rowcount > 0:
            raise ValidationError('This flag_val is aready in here')

class KeyDeleteForm(FlaskForm):
    problem_id = IntegerField('Prob_ID', validators=[DataRequired()])
    flag_round = IntegerField('flag_round', validators=[DataRequired()])
    submit = SubmitField('input Key')


class KeyListForm(FlaskForm):
    problem_id = IntegerField('Prob_ID', validators=[DataRequired()])
    flag_round = IntegerField('flag_round', validators=[DataRequired()])
    submit = SubmitField('input Key')


class ProbInsertForm(FlaskForm):
    problem_id = IntegerField('Prob_ID', validators=[DataRequired()])
    problem_name = StringField('Prob_Name', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_problem_id(self, problem_id):
        Prob = problem.query.filter_by(problem_id=problem_id.data).first()
        if Prob is not None:
            raise ValidationError('This problem_id is aready in here')


class ProbDeleteForm(FlaskForm):
    problem_id = IntegerField('Prob_ID', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_problem_id(self, problem_id):
        Prob = problem.query.filter_by(problem_id=problem_id.data).first()
        if Prob is None:
            raise ValidationError('This problem_id does not exist')


class ProbListForm(FlaskForm):
    problem_id = IntegerField('Prob_ID', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_problem_id(self, problem_id):
        Prob = problem.query.filter_by(problem_id=problem_id.data).first()
        if Prob is None:
            raise ValidationError('This problem_id does not exist')


class RoundInsertForm(FlaskForm):
    round_number = IntegerField('Round_Num', validators=[DataRequired()])
    rount_start = DateTimeField('Rount_Start', format="%Y-%m-%d %H:%M:%S", validators=[DataRequired()])
    rount_end = DateTimeField('Rount_End', format="%Y-%m-%d %H:%M:%S", validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_round_number(self, round_number):
        Round = db.engine.execute('select * from round_time where round_number = ' + str(round_number.data))
        if Round is not None:
            raise ValidationError('This round_number is aready in here')


class RoundDeleteForm(FlaskForm):
    round_number = IntegerField('Round_Num', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_round_number(self, round_number):
        Round = db.engine.execute('select * from round_time where round_number = ' + str(round_number.data))
        if Round is None:
            raise ValidationError('This round_number does not exist')


class RoundListForm(FlaskForm):
    round_number = IntegerField('Round_num', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_round_number(self, round_number):
        Round = db.engine.execute('select * from round_time where round_number = ' + str(round_number.data))
        if Round is None:
            raise ValidationError('This round_number does not exist')


# for test not a real function to be served
class FlagStolenInsertForm(FlaskForm):
    problem_id = IntegerField('Prob_ID', validators=[DataRequired()])
    flag_stolen_id = IntegerField('Flag_stolen_ID', validators=[DataRequired()])
    ids = StringField('ids', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_problem_id(self, problem_id):
        Prob = problem.query.filter_by(problem_id=problem_id.data).first()
        if Prob is None:
            raise ValidationError('This problem_id does not exist')


# for test not a real function to be served
class FlagStolenDeleteForm(FlaskForm):
    problem_id = IntegerField('Prob_ID', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_problem_id(self, problem_id):
        Prob = flag_stolen.query.filter_by(problem_id=problem_id.data).first()
        if Prob is None:
            raise ValidationError('This problem_id does not exist')


class FlagStolenListForm(FlaskForm):
    problem_id = IntegerField('Prob_ID', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_problem_id(self, problem_id):
        Prob = problem.query.filter_by(problem_id=problem_id.data).first()
        if Prob is None:
            raise ValidationError('This problem_id does not exist')


class DatetimeSearchForm(FlaskForm):
    time_start = DateTimeField('time_Start', format="%Y-%m-%d %H:%M:%S", validators=[DataRequired(), InputRequired()])
    time_end = DateTimeField('time_End', format="%Y-%m-%d %H:%M:%S", validators=[DataRequired(), InputRequired()])
    page = IntegerField('page', validators=[DataRequired(), InputRequired()])
    submit = SubmitField('input Key')



class DstIpSearchForm(FlaskForm):
    dst_ip = StringField('dst_ip', validators=[DataRequired()])
    dst_port = IntegerField('dst_port', validators=[DataRequired()])
    page = IntegerField('page', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_dst_ip(self, dst_ip):
        if IpParser(dst_ip.data) is -1:
            raise ValidationError('Wrong input')


class SrcIpSearchForm(FlaskForm):
    src_ip = StringField('src_ip', validators=[DataRequired()])
    src_port = IntegerField('src_port', validators=[DataRequired()])
    page = IntegerField('page', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_src_ip(self, src_ip):
        if IpParser(src_ip.data) is -1:
            raise ValidationError('Wrong input')


class AllSearchForm(FlaskForm):
    rawIpOne = StringField('rawIpOne', validators=[DataRequired()])
    PortOne = IntegerField('PortOne', validators=[DataRequired()])
    rawIpTwo = StringField('rawIpTwo', validators=[DataRequired()])
    portTwo = IntegerField('portTwo', validators=[DataRequired()])
    page = IntegerField('page', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_rawIpOne(self, rawIpOne):
        if IpParser(rawIpOne.data) is -1:
            raise ValidationError('Wrong input')

    def validate_rawIpTwo(self, rawIpTwo):
        if IpParser(rawIpTwo.data) is -1:
            raise ValidationError('Wrong input')

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import flag_table, problem, round_time, flag_stolen



class RegistrationForm(FlaskForm):
    flag_val = StringField('Key', validators=[DataRequired()])
    flag_round = IntegerField('Round', validators=[DataRequired()])
    problem_id = IntegerField('Prob', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_flag_val(self, flag_val):
        Key = flag_table.query.filter_by(flag_val=flag_val.data).first()
        if Key is not None:
            raise ValidationError('This flag_val is aready in here')


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
        Round = round_time.query.filter_by(round_number=round_number.data).first()
        if Round is not None:
            raise ValidationError('This round_number is aready in here')


class RoundDeleteForm(FlaskForm):
    round_number = IntegerField('Round_Num', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_round_number(self, round_number):
        Round = round_time.query.filter_by(round_number=round_number.data).first()
        if Round is None:
            raise ValidationError('This round_number does not exist')


class RoundListForm(FlaskForm):
    round_number = IntegerField('Round_num', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_round_number(self, round_number):
        Round = round_time.query.filter_by(round_number=round_number.data).first()
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

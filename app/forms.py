from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import flag_table, problem



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

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import flag_table



class RegistrationForm(FlaskForm):
    flag_val = StringField('Key', validators=[DataRequired()])
    flag_round = IntegerField('Round', validators=[DataRequired()])
    problem_id = IntegerField('Prob', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_Key(self, flag_table):
        Key = flag_table.query.filter_by(flag_val=flag_val.data).first()
        if Key is not None:
            raise ValidationError('This flag_val is aready in here')
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Key



class RegistrationForm(FlaskForm):
    Key = StringField('Key', validators=[DataRequired()])
    Round = StringField('Round', validators=[DataRequired()])
    Prob = StringField('Prob', validators=[DataRequired()])
    submit = SubmitField('input Key')

    def validate_Key(self, Key):
        Key = Key.query.filter_by(Key=Key.data).first()
        if Key is not None:
            raise ValidationError('This Key is aready in here')

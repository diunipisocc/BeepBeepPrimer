from flask_wtf import FlaskForm
import wtforms as f
import monolith.form_custom_models as fc
from wtforms.validators import DataRequired, NumberRange
from monolith.form_custom_models import UniqueMailValidator

class LoginForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired()])
    password = f.PasswordField('password', validators=[DataRequired()])
    display = ['email', 'password']


class RemoveUserForm(FlaskForm):
    # email = f.StringField('email', validators=[DataRequired()])
    password = f.PasswordField('password', validators=[DataRequired()])
    # display = ['email', 'password']
    display = ['password']


class UserForm(FlaskForm):
    email     = f.StringField('Email', validators=[DataRequired(),
                                                   UniqueMailValidator()])
    firstname = f.StringField('Firstname')
    lastname  = f.StringField('Lastname')
    password  = f.PasswordField('Password', validators=[DataRequired()])
    age       = f.IntegerField('Age')
    weight    = f.FloatField('Weight')
    max_hr    = f.IntegerField('Max Heartrate')
    rest_hr   = f.IntegerField('Rest Heartrate')
    vo2max    = f.FloatField('VO2 Max')

    display = ['email',
               'firstname',
               'lastname',
               'password',
               'age',
               'weight',
               'max_hr',
               'rest_hr',
               'vo2max']

class ProfileForm(UserForm):
  def __init__(self, **kwargs):
        UserForm.__init__(self, **kwargs)
        self['email'].validators = [DataRequired()]
        self['password'].validators = []
        self['password'].flags.required = False
        
   
class TrainingObjectiveSetterForm(FlaskForm):
    start_date = f.DateField('Start date',
                             validators=[DataRequired(message='Not a valid date format'), 
                                         fc.NotLessThenToday()],
                             widget=f.widgets.Input(input_type="date"))
    end_date = f.DateField('End date',
                           validators=[DataRequired(message='Not a valid date format'),
                                       fc.NotLessThan('start_date', message='End date must not be less than Start date'),
                                       fc.NotLessThenToday()],
                           widget=f.widgets.Input(input_type="date"))
    kilometers_to_run = f.FloatField('Kilometers to run',
                                     validators=[DataRequired('You need at least a meter to run'),
                                                 NumberRange(min=0.001, message='You need at least a meter to run')],
                                     widget=fc.FloatInput(step='any', min_='0'),
                                     filters=[lambda value: float('%.3f' % float(value)) if value is not None else value])

    display = ['start_date', 'end_date', 'kilometers_to_run']

class TrainingObjectiveVisualizerForm(FlaskForm):
    start_date = f.DateField('Start date')
    end_date = f.DateField('End date')
    kilometers_to_run = f.FloatField('Kilometers to run')
    traveled_kilometers = f.FloatField('Traveled kilometers')
    status = f.StringField('Status')
    description = f.StringField('Description')

    display = ['start_date', 'end_date', 'kilometers_to_run', 'traveled_kilometers', 'status', 'description']

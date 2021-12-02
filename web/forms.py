from wtforms import Form, StringField, SelectField, DateField, IntegerField, FloatField
from wtforms.validators import NumberRange, InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from Logic.database import Session
from Logic import Contract, User


def useres():
  session = Session()
  return session.query(User)
  

# contract_rate_choices = [(0, '🌚🌚🌚🌚🌚'), (1, '🌞🌚🌚🌚🌚'), (2, '🌞🌞🌚🌚🌚'), (3, "🌞🌞🌞🌚🌚"), (4, "🌞🌞🌞🌞🌚"), (5, "🌞🌞🌞🌞🌞")]
contract_rate_choices = [(5, "🌞🌞🌞🌞🌞"), (4, "🌞🌞🌞🌞🌚"), (3, "🌞🌞🌞🌚🌚"), (2, '🌞🌞🌚🌚🌚'), (1, '🌞🌚🌚🌚🌚'), (0, '🌚🌚🌚🌚🌚')]

class ContractForm(Form):
  name = StringField('Название')
  owner = QuerySelectField('Владелец', query_factory=useres, validators=[InputRequired()])
  tenant = QuerySelectField('Арендатор', query_factory=useres, validators=[InputRequired()])
  provider = QuerySelectField('Провайдер', query_factory=useres, validators=[InputRequired()])

  start_date = DateField("Начало", validators=[InputRequired()])
  end_date = DateField("Конец", validators=[InputRequired()])

  owner_rate_tenant = SelectField("Арендатору", choices=contract_rate_choices, validators=[NumberRange(0, 5), InputRequired()])
  owner_rate_provider = SelectField("Провайдеру", choices=contract_rate_choices,validators=[NumberRange(0, 5), InputRequired()])

  tenant_rate_owner = SelectField("Владельцу", choices=contract_rate_choices, validators=[NumberRange(0, 5), InputRequired()])
  tenant_rate_provider = SelectField("Провайдеру", choices=contract_rate_choices, validators=[NumberRange(0, 5), InputRequired()])

  provider_rate_tenant = SelectField("Арендатору",choices=contract_rate_choices,  validators=[NumberRange(0, 5), InputRequired()])
  provider_rate_owner = SelectField("Владельцу",choices=contract_rate_choices,  validators=[NumberRange(0, 5), InputRequired()])

  

class UserForm(Form):
  name = StringField('Имя пользователя', validators=[InputRequired()])


class CalculateDataForm(Form):

  s_coef = FloatField("s коэффициент", validators=[InputRequired()])
  u_coef = FloatField("u коэффициент", validators=[InputRequired()])
  time_lower = IntegerField("t0 (нижний порог времени)", validators=[InputRequired()])
  time_higher = IntegerField("t1 (верхний порог времени)", validators=[InputRequired()])
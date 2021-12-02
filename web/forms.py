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
  name = StringField('Title')
  owner = QuerySelectField('Owner', query_factory=useres, validators=[InputRequired()])
  tenant = QuerySelectField('Tenant', query_factory=useres, validators=[InputRequired()])
  provider = QuerySelectField('Provider', query_factory=useres, validators=[InputRequired()])

  start_date = DateField("Start Date", validators=[InputRequired()])
  end_date = DateField("End Date", validators=[InputRequired()])

  owner_rate_tenant = SelectField("Rate Tenant", choices=contract_rate_choices, validators=[NumberRange(0, 5), InputRequired()])
  owner_rate_provider = SelectField("Rate Provider", choices=contract_rate_choices,validators=[NumberRange(0, 5), InputRequired()])

  tenant_rate_owner = SelectField("Rate Owner", choices=contract_rate_choices, validators=[NumberRange(0, 5), InputRequired()])
  tenant_rate_provider = SelectField("Rate Provider", choices=contract_rate_choices, validators=[NumberRange(0, 5), InputRequired()])

  provider_rate_tenant = SelectField("Rate Tenant",choices=contract_rate_choices,  validators=[NumberRange(0, 5), InputRequired()])
  provider_rate_owner = SelectField("Rate Provider",choices=contract_rate_choices,  validators=[NumberRange(0, 5), InputRequired()])

  

class UserForm(Form):
  name = StringField('User name', validators=[InputRequired()])


class CalculateDataForm(Form):
  s_coef = FloatField("s coefficient", validators=[InputRequired()])
  u_coef = FloatField("u coefficient", validators=[InputRequired()])
  time_lower = IntegerField("Time lower bound (t0)", validators=[InputRequired()])
  time_higher = IntegerField("Time heigher bound (t1)", validators=[InputRequired()])
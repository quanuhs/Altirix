from flask import Flask, _app_ctx_stack, url_for, render_template, redirect, request
from flask import session as user_session

from flask_cors import CORS
from sqlalchemy.orm import scoped_session

from web.forms import ContractForm, UserForm, CalculateDataForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

from data_manipulation import simulate
import config
from Logic import User, Rating, Contract
from Logic.database import Session, create_db





app = Flask(__name__,
            static_folder=config.PATH_TO_STATIC,
            template_folder=config.PATH_TO_TEMPLATES)


CORS(app)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = 'somesecretkeytosignsessions'
app.session = scoped_session(Session, scopefunc=_app_ctx_stack.__ident_func__)

admin = Admin(app, name='Admin panel', template_mode='bootstrap4')
admin.add_view(ModelView(User, app.session))
admin.add_view(ModelView(Contract, app.session))




@app.route('/', methods=["POST", "GET"])
def main_page():
  is_error = request.args.get("is_error")

  if user_session.get("s_coef") is None:
    user_session["s_coef"] = 1.0
  
  if user_session.get("u_coef") is None:
    user_session["u_coef"] = 1.0
  
  if user_session.get("time_lower") is None:
    user_session["time_lower"] = 1.0

  if user_session.get("time_higher") is None:
    user_session["time_higher"] = 5.0

  users = app.session.query(User).all()
  
  counting_data = {"s_coef": user_session.get("s_coef"), "u_coef": user_session.get("u_coef"), "time_lower": user_session.get("time_lower"), "time_higher": user_session.get("time_higher")}


  return render_template("index.html", users=users, counting_data=counting_data, is_error=is_error)



@app.route('/user/<user_id>')
def user_page(user_id):

  try:
    user_id = int(user_id)
    
    user = app.session.query(User).filter(User.id == user_id).one_or_none()


    if user:
      data = simulate.simulate(user, 5, user_session["s_coef"], user_session["u_coef"], user_session["time_lower"], user_session["time_higher"])
      labels = {"owner": [i+1 for i in range(len(data.get("owner")))],"tenant": [i+1 for i in range(len(data.get("tenant")))], "provider": [i+1 for i in range(len(data.get("provider")))]}

      return render_template("user_page.html", user=user, data=data, labels=labels)
  
  except Exception as e:
    print(e)
  
    return redirect(url_for('main_page', is_error = e))

  return redirect(url_for('main_page'))



@app.route('/create/contract', methods=["POST", "GET"])
def create_contract_page():
  form = ContractForm(request.form)



  if request.method == "POST":
    owner = form["owner"].data
    tenant = form["tenant"].data
    provider = form["provider"].data

    start_date = form["start_date"].data
    end_date = form["end_date"].data

    _contract = Contract(owner.id, tenant.id, provider.id, start_date, end_date)
    app.session.add(_contract)
    _contract.rate_all((form["owner_rate_tenant"].data, form["owner_rate_provider"].data),(form["tenant_rate_owner"].data, form["tenant_rate_provider"].data),(form["provider_rate_owner"].data, form["provider_rate_tenant"].data))
    
    app.session.commit()

    if request.form.get("action") == "save":
      return redirect(url_for('main_page'))
    else:
      return render_template("add_contract.html", form=form, is_dublicated=True)

  return render_template("add_contract.html", form=form)



@app.route('/create/user', methods=["POST", "GET"])
def create_user_page():
  form = UserForm(request.form)

  if request.method == "POST":
    user_name = form["name"].data

    app.session.add(User(user_name))
    app.session.commit()
    return redirect(url_for('main_page'))

  return render_template("add_user.html", form=form)



@app.route("/settings", methods=["POST", "GET"])
def change_settings():
  form = CalculateDataForm(request.form)
  counting_data = {"s_coef": user_session.get("s_coef"), "u_coef": user_session.get("u_coef"), "time_lower": user_session.get("time_lower"), "time_higher": user_session.get("time_higher")}

  if request.method == "POST":
    user_session["s_coef"] = form["s_coef"].data
    user_session["u_coef"] = form["u_coef"].data
    user_session["time_lower"] = form["time_lower"].data
    user_session["time_higher"] = form["time_higher"].data

    return redirect(url_for('main_page'))


  return render_template("change_settings.html", form = form, counting_data=counting_data)



if __name__ == '__main__':
  
    db_is_created = os.path.exists(config.DATABASE_NAME)
    if not db_is_created:
      create_db()
    
    app.run(host=config.HOST_ADDRESS, port=config.HOST_PORT, ssl_context=('/etc/letsencrypt/live/twinsharing.com/fullchain.pem', '/etc/letsencrypt/live/twinsharing.com/privkey.pem'))

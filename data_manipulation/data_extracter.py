
from Logic import User, Contract, Rating
from Logic.database import Session
from sqlalchemy import desc

def prepare_owner_data(owner_contracts):
  tenant_owner_contracts = {}

  for contract in owner_contracts:
    if tenant_owner_contracts.get(contract.tenant_id) == None:
      tenant_owner_contracts[contract.tenant_id] = []
    
    tenant_owner_contracts[contract.tenant_id].append(contract)
  
  return tenant_owner_contracts


def reshape_owner_data(user_id, tenant_owner_contracts):
  session = Session()
  tenants_durations, tenants_rates, providers_rates = [], [], []

  for _key in tenant_owner_contracts:
    contracts = tenant_owner_contracts[_key]
    provider_rate = session.query(Rating).join(Contract).filter(Rating.target_id == user_id, Rating.contract_id.in_([x.id for x in contracts]), Contract.id == Rating.contract_id, Contract.owner_id == Rating.target_id, Contract.provider_id == Rating.rater_id).order_by(desc(Rating.contract_id)).all()

    tenant_rate = session.query(Rating).join(Contract).filter(Rating.rater_id == _key, Rating.target_id == user_id, Rating.contract_id.in_([x.id for x in contracts]), Contract.id == Rating.contract_id, Contract.owner_id == Rating.target_id, Contract.tenant_id == Rating.rater_id).order_by(desc(Rating.contract_id)).all()

    if len(tenant_rate) > 0:
      tenants_durations.append([x.duration for x in contracts])
      tenants_rates.append([x.rate for x in tenant_rate])
      providers_rates.append([x.rate for x in provider_rate])

  session.close()

  return tenants_durations, tenants_rates, providers_rates


def get_owner_data(user_id):
  session = Session()
  owner:User = session.query(User).filter(User.id == user_id).one_or_none()
  owner_contracts = owner.owner_contracts
  
  tenant_owner_contracts = prepare_owner_data(owner_contracts)
  session.close()
  return reshape_owner_data(user_id, tenant_owner_contracts)



def prepare_tenant_data(tenant_contracts):
  tenant_user_contracts = {}

  for contract in tenant_contracts:
    if tenant_user_contracts.get(contract.owner_id) == None:
      tenant_user_contracts[contract.owner_id] = []
    
    tenant_user_contracts[contract.owner_id].append(contract)
  
  return tenant_user_contracts

def reshape_tenant_data(user_id, tenant_user_contracts):
  owners_durations, owners_rates, providers_rates = [], [], []
  session = Session()

  for _key in tenant_user_contracts:
    contracts = tenant_user_contracts[_key]

    # Собираем и подготавливаем данные
    provider_rate = session.query(Rating).join(Contract).filter(Rating.target_id == user_id, Rating.contract_id.in_([x.id for x in contracts]), Contract.id == Rating.contract_id, Contract.tenant_id == Rating.target_id, Contract.provider_id == Rating.rater_id).order_by(desc(Rating.contract_id)).all()

    owner_rate = session.query(Rating).join(Contract).filter(Rating.rater_id == _key, Rating.target_id == user_id, Rating.contract_id.in_([x.id for x in contracts]), Contract.id == Rating.contract_id, Contract.tenant_id == Rating.target_id, Contract.owner_id == Rating.rater_id).order_by(desc(Rating.contract_id)).all()

    if len(provider_rate) > 0:
      owners_durations.append([x.duration for x in contracts])
      owners_rates.append([x.rate for x in owner_rate])
      providers_rates.append([x.rate for x in provider_rate])

  session.close()

  return owners_durations, owners_rates, providers_rates



def get_tenant_data(user_id):
  session = Session()
  tenant:User = session.query(User).filter(User.id == user_id).one_or_none()
  tenant_contracts = tenant.tenant_contracts

  tenant_user_contracts = prepare_tenant_data(tenant_contracts)
  session.close()
  return reshape_tenant_data(user_id, tenant_user_contracts)



def get_provider_data(user_id):
  session = Session()
  provider:User = session.query(User).filter(User.id == user_id).one_or_none()

  tenant_rated_provider = session.query(Rating).join(Contract).filter(Rating.target_id == user_id, Rating.rater_id == Contract.tenant_id, Contract.provider_id == Rating.target_id).order_by(desc(Rating.contract_id)).all()

  owner_rated_provider = session.query(Rating).join(Contract).filter(Rating.target_id == provider.id, Rating.rater_id == Contract.owner_id, Contract.provider_id == Rating.target_id).order_by(desc(Rating.contract_id)).all()
  

  return [x.rate for x in tenant_rated_provider], [x.rate for x in owner_rated_provider]



def get_user_by_id(user_id):
  session = Session()
  user:User = session.query(User).filter(User.id == user_id).one_or_none()

  session.close()
  return user
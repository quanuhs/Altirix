from counter import Counter

from data_manipulation import data_extracter as extr


def simulate(user, rating, s_coef, u_coef, time_lower, time_higher):
  calculate = Counter(rating, s_coef, u_coef, time_lower, time_higher)


  data = {"owner": [], "tenant": [], "provider": []}

  owner_contracts = user.owner_contracts
  owner_contracts.reverse()

  tenant_contracts = user.tenant_contracts
  tenant_contracts.reverse()

  provider_contracs = extr.get_provider_data(user.id)
  provider_contracs[0].reverse()
  provider_contracs[1].reverse()


  for i in range(len(owner_contracts)):
    data["owner"].append(calculate.count_owner_rating(*extr.reshape_owner_data(user.id, extr.prepare_owner_data(owner_contracts[:i+1]))))
  
  for i in range(len(tenant_contracts)):
    data["tenant"].append(calculate.count_tenant_rating(*extr.reshape_tenant_data(user.id, extr.prepare_tenant_data(tenant_contracts[:i+1]))))

  for i in range(len(provider_contracs[0])):
      data["provider"].append(calculate.count_provider_rating(provider_contracs[0][:i+1], provider_contracs[1][:i+1]))
  
  
  return data

class Counter:
  # Подсчитывает рейтинг Владельца - owner, Арендатора - tenant, Провайдера - provider

  def __init__(self, max_points, s_coef, u_coef, time_lower, time_higher, _round=3):
    self.max_points = max_points
    self.s_coef = s_coef
    self.u_coef = u_coef
    self.time_lower = time_lower
    self.time_heigher = time_higher
    self._round = _round

    self.provider_x_coef = 0.7
    self.provider_y_coef = 0.3
  

  def get_weight(self, occupation_time) -> float:
    if occupation_time <= self.time_lower:
      return 0.0
    
    if occupation_time >= self.time_heigher:
      return 1.0
    
    return float(occupation_time-self.time_lower)/(self.time_heigher - self.time_lower)
  


  def get_owner_coef(self, tenant_rated_owner_amount, tenant_durations, tenant_rates, provider_rates) -> float:
    a = 0.0

    for j in range(tenant_rated_owner_amount):
      js = 1/(j+1)**self.s_coef
      t = tenant_durations[j]
      u = self.get_weight(t)
      x = tenant_rates[j]
      z = provider_rates[j]

      a += 2 * ( js + (1 - js) * u ) * x + z
    
    return a



  def get_tenant_coef(self, owner_rated_tenant_amount, owner_durations, owner_rates, provider_rates) -> float:
    b = 0.0

    for j in range(owner_rated_tenant_amount):
      js = 1/(j+1)**self.u_coef
      t = owner_durations[j]
      u = self.get_weight(t)
      y = owner_rates[j]
      w = provider_rates[j]

      b += (1/2 + u/3)*(js + (1 - js) * u) * y + (1/2 - u/3) * w

    return b


  def get_provider_coef(self, tenants_rates, owners_rates) -> float:
    
    a = 0.0

    contracts_amount = len(tenants_rates)

    if contracts_amount == 0:
      return a

    for j in range(contracts_amount):
      x:float = tenants_rates[j]
      y:float = owners_rates[j]

      a += self.provider_x_coef*x + self.provider_y_coef*y
    
    a *= 1/(self.max_points * contracts_amount)

    return round(a, self._round)



  def count_tenant_rating(self, owners_durations, owners_rates, providers_rates) -> float:
    # Все переменные вложенные списки: [[1, 2, ...], [1] ...] каждая позиция соответствует арендателю.
   
    p = 0.0

    if len(owners_durations) == 0:
      return p

    for i in range(len(owners_rates)):
      owner_durations = owners_durations[i]
      owner_rates = owners_rates[i]
      provider_rates = providers_rates[i]
      
      r = len(owner_durations)
      b = self.get_tenant_coef(r, owner_durations, owner_rates, provider_rates)

      p += b/r

    p *= 1/len(owners_durations)

    return round(p, self._round)

  
  def count_provider_rating(self, tenants_rates, owners_rates) -> float:
    return self.get_provider_coef(tenants_rates, owners_rates)


  
  def count_owner_rating(self, tenants_durations, tenants_rates, providers_rates) -> float:
    # Все переменные вложенные списки: [[1, 2, ...], [1] ...] каждая позиция соответствует арендателю.

    q = 0.0

    if len(tenants_durations) == 0:
      return q

    for i in range(len(tenants_rates)):
      tenant_durations = tenants_durations[i]
      tenant_rates = tenants_rates[i]
      provider_rates = providers_rates[i]

      m = len(tenant_durations)
      a = self.get_owner_coef(m, tenant_durations, tenant_rates, provider_rates)

      q += a/(3*m)

    q *= 1/len(tenants_rates)

    return round(q, self._round)
      


  def count_price_coef_owner(self, owner_coef, tenant_coef, provider_coef) -> float:
    l = 1 - provider_coef

    to = tenant_coef+owner_coef
    if to == 0:
      return 0
    
    return round((l/2 + (((1-l)*tenant_coef)/(to))), self._round)


  def count_price_coef_tenant(self, owner_coef, tenant_coef, provider_coef) -> float:
    l = 1 - provider_coef
    
    to = tenant_coef+owner_coef
    if to == 0:
      return 0

    return round((l/2 + (((1-l)*owner_coef)/(to))), self._round)
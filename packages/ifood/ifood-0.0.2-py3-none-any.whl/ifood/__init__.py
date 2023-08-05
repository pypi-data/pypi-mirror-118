import requests

class Ifood:

  local = ''
  items = ''

  def __init__(self,zipCode):
    self.__zipCode = zipCode
    self.searchAddress()

  def searchAddress(self):
    url = f"https://marketplace.ifood.com.br/v1/addresses:geocode?query={self.__zipCode}"
    headers = {
      'x-application-key': '54z2laLEcZ0gzfERl27dEu1N',
      'x-ifood-session-id': 'd21c2c76-2518-44f9-9e1c-9435376dcfad'
    }
    response = requests.request("GET", url, headers=headers, data={})
    self.local = response.json()['addresses']
    return self.local

  def city(self):
    return self.local[0]['city']

  def state(self):
    return self.local[0]['state']

  def country(self):
    return self.local[0]['country']

  def streetName(self):
    return self.local[0]['streetName']

  def latitude(self):
    return self.local[0]['coordinates']['latitude']

  def longitude(self):
    return self.local[0]['coordinates']['longitude']

  def postalCode(self):
    return self.local[0]['postalCode']

  def searchItems(self,product):
    self.product = product
    lat = self.latitude()
    lng = self.longitude()
    url = f'https://marketplace.ifood.com.br/v2/search/catalog-items?latitude={lat}&longitude={lng}&channel=IFOOD&term={self.product}&size=100&page=0'
    response = requests.request("GET", url, headers={}, data={})
    self.items = response.json()['items']['data']
    return self.items

  def listItems(self):
    result = []
    keys = ['id','name','category','price','merchant','slug','distance','deliveryTime','deliveryValue','mainCategoryName']
    for x in self.items:
      values = []
      values.append(x['id'])
      values.append(x['name'])
      values.append(x['category']['name'])
      values.append(x['price'])
      values.append(x['merchant']['name'])
      values.append(x['merchant']['slug'])
      values.append(x['merchant']['distance'])
      values.append(x['merchant']['deliveryTime'])
      values.append(x['merchant']['deliveryFee']['value'])
      values.append(x['merchant']['mainCategory']['name'])
      result.append(dict(zip(keys,values)))
    return result



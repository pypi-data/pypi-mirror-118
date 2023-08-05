# Ifood

## To install

```
pip install ifood
```

## To import the library

```
from ifood import Ifood
```

## Defining the zip code

```
app = Ifood('59082311') 
```

## or address

```
app = Ifood('rua+buzius+47+brazil') 
```

## Creating object to search address

```
print(app.searchAddress())
```

## All functions of address

```
print(app.city())
print(app.state())
print(app.country())
print(app.streetName())
print(app.postalCode())
print(app.latitude())
print(app.longitude())
```

## Creating object to search product

```
app.searchItems('energetico+reign')
```

## All functions of product

```
print(app.listItems())
print(app.listItems()[0]['id'])
print(app.listItems()[0]['name'])
print(app.listItems()[0]['category'])
print(app.listItems()[0]['price'])
print(app.listItems()[0]['merchant'])
print(app.listItems()[0]['slug'])
print(app.listItems()[0]['distance'])
print(app.listItems()[0]['deliveryTime'])
print(app.listItems()[0]['deliveryValue'])
print(app.listItems()[0]['mainCategoryName'])
```

## Links

See my [GitHub](https://github.com/claudiotorresarbe).

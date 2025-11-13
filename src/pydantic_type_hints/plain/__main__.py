import logging
from .product import ProductFactory
from .furniture import TableCategory

logging.basicConfig(level=logging.INFO)

category = TableCategory('furniture','table','dining-table')
print([ k for k in vars(category).keys()])

rawData = {'family':'furniture','category':'table','tableCategory':'dining-table','title':'Dining Table'}

product = ProductFactory.buildFromDict(rawData)
print(type(product))
print(product)
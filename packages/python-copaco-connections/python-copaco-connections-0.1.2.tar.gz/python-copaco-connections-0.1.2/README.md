# python-copaco-connections
Easy python integrations for the Copaco Customer Connections

## Limitations

This package is limited to the Copaco BE - Dutch Productlist in CSV format via FTP. Might be extended in the future.

More info here: https://www.copaco.com/en-be/customer-service-e-commerce-fulfillment

## Getting started

### Install

Install with pip.

```python
pip install python-copaco-connections
```

### Import

Import the package and the CopacoConnectionBE object.

```python
from copaco.connection import CopacoConnectionBE
```

### Setup connection

Make the connection with your provided FTP credentials.

```python
conn = CopacoConnectionBE(FTP_HOST, FTP_LOGIN, FTP_PASSWD)
```


## Pricelist

You can retrieve the pricelist as follows:

```python
priceList = conn.priceList.get()
```

This will return an ordinary list which contains PriceListItem objects.

You can find the attributes of this object and their use below:

**PriceListItem object**

| Attribute  | Contains |
| ------------- | ------------- |
| article  | Article number  |
| vendorCode  | Unique vendor code  |
| description  | Short description  |
| price  | Price, excluding levies  |
| priceWithLevies  | Price, including levies |
| stock  | Amount of stock available  |
| hierarchy  | Product hierarchy  |
| unspscCode  | UNSPSC code  |
| EAN  | EAN code  |
| statusCode  | Status code (0 - 12). Refer to docs.  |
| status  | Human-readable status  |
| auvibel  | Price of Auvibel  |
| reprobel  | Price of Reprobel  |
| recupel  | Price of Recupel  |
| bebat  | Price of Bebat  |
| nextDelivery  | Next delivery date of this product |
| nextDeliveryAmount  | Amount that will be delivered on next delivery |
| inventoryStatusCode  | ATP code |
| inventoryStatus  | Human-readable ATP code |


## Sample script

Show all articles with their prices, including levies.

```python
from copaco.connection import CopacoConnectionBE

HOST = 'ftp.copaco.com'
LOGIN = 'XXXX'
PASSWD = 'XXXX'

conn = CopacoConnectionBE(HOST, LOGIN, PASSWD)

priceList = conn.priceList.get()
for item in priceList:
  formattedStr = '{description} - {number} - € {price}'.format(description=item.description, number=item.article, price=item.priceWithLevies)
  print(formattedStr)

```

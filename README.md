# playwright-flask_restful-api
An API built in Flask-RESTful that uses playwright-python to scrape laptops info from [webscraper.io](https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops)

# Usage
Clone the repo:
```
git clone https://github.com/hbtalha/playwright-flask_restful-api.git
cd playwright-flask_restful-api
pip install -r requirements.txt
```

Run the server
```
python app.py
```
# User endpoints
Returns all laptops:

GET http://127.0.0.1:5000/laptops

### GET parameters:

```yaml
Get laptops
---
tags:
  - Laptops

parameters:
  - name: brands
    in: query
    type: string|list
    required: false
    description: brands of the laptop
  - name: sort
    in: query
    type: string
    required: false
    description: sort laptops by one following options:'brand', 'price', 'num_reviews', 'num_stars
  - name: sorting_order
    in: query
    type: string
    required: false
    description: sorting order ('ascending', 'descending')
  - name: num
    in: query
    type: integer
    required: false
    description: number of laptops to get
  - name: min_num_stars
    in: query
    type: integer
    required: false
    description: get laptop with the minimum number of stars
  - name: min_num_reviews
    in: query
    type: integer
    required: false
    description: get laptop with the minimum number of reviews
  - name: min_price
    in: query
    type: integer|float
    required: false
    description: get laptop with the minimum price
  - name: max_price
    in: query
    type: integer|float
    required: false
    description: get laptop with the maximum price
responses:
  400:
    description: Errors {'Unknown sort option', 'number of laptops must be greater than zero', 'invalid price range'}
  200:
    description: laptops returned successfully

```

### example code of GET request with parameters:
```python
import json
import requests

BASE = 'http://127.0.0.1:5000/'

# response = requests.get(BASE + 'laptops') # returns all laptops

response = requests.get(BASE + 'laptops', {"brands": ['asus', 'hp'], "sort": "price", "sorting_order":'ascending', "num": 15, "max_price": 1500, "min_price": 400, "min_num_reviews": 5,
 "min_num_stars": 2})

print(response.json())
with open('D:/Desktop/response.json', 'w') as f:
    f.write(json.dumps(response.json()))
```

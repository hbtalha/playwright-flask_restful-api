from flask import Flask
from flask_restful import Api
from resources.laptop import Laptop
# from flasgger import Swagger
# from config.swagger import template, swagger_config

app = Flask(__name__)
api = Api(app)

'''On hold for now'''
# app.config['SWAGGER'] = {
#     'title': 'Laptops Api',
#     'uiversion': 3.0,
#     "specs_route": "/swagger/"
# }

'''On hold for now'''
# Swagger(app, config=swagger_config, template=template)

api.add_resource(Laptop, '/laptops')

if __name__ == "__main__":
    app.run(port=8000)
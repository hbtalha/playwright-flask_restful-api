template = {
    "swagger": "3.0",
    "info": {
        "title": "Laptops API",
        "description": "Grab laptops info from https://webscraper.io/test-sites/e-commerce/allinone",
        "version": "0.1.1",
        "contact": {
            "name": "HBatalha",
            "email": "helderbatalha3@gmail.com",
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}

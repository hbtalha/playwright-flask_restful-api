from constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from scraper.grabber import Grabber
from flask_restful import Resource, abort
from flask import request as flask_request
# from flasgger import swag_from
import sys
sys.path.append('./')

class Laptop(Resource):
    def __init__(self) -> None:
        self.grabber: Grabber = Grabber()
        self.laptops_sort = ['brand', 'price', 'num_reviews', 'num_stars']

    def abort_if_sort_option_invalid(self, sort):
        if sort is not None and sort not in self.laptops_sort:
            abort(HTTP_400_BAD_REQUEST, message="Unknown sort option {0}, allowed options: {1}".format(sort, self.laptops_sort))

    def abort_if_num_is_zero_or_less(self, num):
        if num is not None and isinstance(num, int) and num <= 0:
            abort(HTTP_400_BAD_REQUEST, message="number of laptops must be greater than zero")
    
    def validate_price_range(self, min_price, max_price):
        if min_price is not None and max_price is not None:
            if (isinstance(max_price, int) or isinstance(max_price, float)) and (isinstance(min_price, int) or isinstance(min_price, float)):
                if min_price > max_price:
                    abort(HTTP_400_BAD_REQUEST, message="invalid price range: min_price must not be greater than max_price")

    def convert_to_numeric(self, num):
        try:
            return int(num)
        except:
            try:
                return float(num)
            except:
                return None

    # @swag_from('./docs/laptops/laptops.yaml')
    def get(self):
        args = flask_request.args
        self.abort_if_sort_option_invalid(args.get('sort'))
        self.abort_if_num_is_zero_or_less(args.get('num'))
        self.validate_price_range(min_price=args.get('min_price'), max_price=args.get('max_price'))
        brands = args.getlist('brands')
        sort = args.get('sort')
        sorting_order = args.get('sorting_order')
        num = self.convert_to_numeric(args.get('num'))
        min_num_stars = self.convert_to_numeric(args.get('min_num_stars'))
        min_num_reviews = self.convert_to_numeric(args.get('min_num_reviews'))
        max_price = self.convert_to_numeric(args.get('max_price'))
        min_price = self.convert_to_numeric(args.get('min_price'))
        return self.grabber.get_laptops(requested_brands=brands, sort=sort, sorting_order=sorting_order, num=num, max_price=max_price,
                                        min_price=min_price, min_num_of_reviews=min_num_reviews, min_num_of_stars=min_num_stars), HTTP_200_OK

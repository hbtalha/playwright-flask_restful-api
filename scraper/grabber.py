from playwright.sync_api import sync_playwright

class Grabber:
    def __init__(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        self.page.goto('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')
        
        # self.page.goto('https://webscraper.io/test-sites/e-commerce/allinone/product/545')
        # self.page.locator('#side-menu > li:nth-child(2)').click()
        # self.page.locator('#side-menu > li.active > ul > li:nth-child(1)').click()

        self.laptops_sort = ['brand',  '', 'price', '', 'num_reviews', 'num_stars', ] # empty strings to avoid too many if and else statements in filter function
        self.sorting_order = ['ascending', 'descending']
        self.laptop_brands = ['all', 'lenovo', 'dell', 'hp', 'hewlett packard', 'acer', 'asus', 'msi', 'toshiba', 'prestigio']

    def _filter_laptops(self, laptops: list, brands: list, sort: str, sorting_order: str,
                        min_num_of_stars: int, min_num_of_reviews: int, num: int, max_price: int, min_price: int) -> list:
        if laptops:
            if brands is not None and not (len(brands) == 1 and brands[0] == 'all') and any(brand in brands for brand in self.laptop_brands):
                laptops = [laptop for laptop in laptops if laptop[0] is not None and laptop[0].lower() in( brand.lower() for brand in brands)]

            if sort is not None and isinstance(sort, str) and sort.lower() in self.laptops_sort:
                sort_index = None
                try:
                    sort_index = self.laptops_sort.index(sort.lower())
                except:
                    pass

                if sort_index is not None and sorting_order is not None and isinstance(sorting_order, str) and sorting_order.lower() in self.sorting_order:
                    sort_reverse = True if sorting_order == self.sorting_order[1] else False
                    print('sorting = {0} - {1} - {2}'.format(sort_index, sort, sort_reverse))
                    laptops.sort(key=lambda x: x[sort_index], reverse=sort_reverse)

            if min_num_of_stars is not None and isinstance(min_num_of_stars, int) and min_num_of_stars >= 1 and min_num_of_stars <= 5:
                laptops = [laptop for laptop in laptops if laptop[5] is not None and laptop[5] >= min_num_of_stars]

            if min_num_of_reviews is not None and isinstance(min_num_of_reviews, int) and min_num_of_reviews >= 0:
                laptops = [laptop for laptop in laptops if laptop[4] is not None and laptop[4] >= min_num_of_reviews]

            if min_price is not None and (isinstance(min_price, int) or isinstance(min_price, float)):
                laptops = [laptop for laptop in laptops if laptop[2] >= min_price]
            
            if max_price is not None and (isinstance(max_price, int) or isinstance(max_price, float)):
                laptops = [laptop for laptop in laptops if laptop[2] <= max_price]

            if num is not None and isinstance(num, int) and num < len(laptops):
                laptops = laptops[:num]

            return laptops
        else:
            return []

    def get_laptops(self, requested_brands: list, sort: str, sorting_order: str, min_num_of_stars: int, min_num_of_reviews: int, num: int, max_price: int, min_price: int):
        urls = self.page.locator('.caption > h4 > .title').evaluate_all('elements => elements.map(el => el.href)')
        descriptions = self.page.locator('.caption > .description').all_text_contents()
        prices = self.page.locator('.caption > .price').all_text_contents()
        names = self.page.locator('.caption > h4 > .title').all_text_contents()
        num_reviews = self.page.locator('.ratings > .pull-right').all_text_contents()
        star_handles = self.page.locator('.ratings > p:nth-child(2)').element_handles()
        num_stars = []
        for e in star_handles:
            num_stars.append((e.inner_html()).count('class'))

        brands = [name.split()[0] for name in names]
        brands = ["HP" if brand == "Hewlett" else brand for brand in brands]
        prices = [price[1:] for price in prices]
        prices = list(map(float, prices))
        num_reviews = [nr.removesuffix(' reviews') for nr in num_reviews]
        num_reviews = list(map(int, num_reviews))

        all_laptops = list(zip(brands, names, prices, descriptions, num_reviews, num_stars, urls))
        filtered_laptops = self._filter_laptops(laptops=all_laptops, brands=requested_brands, sort=sort, sorting_order=sorting_order, min_num_of_stars=min_num_of_stars,
                                                min_num_of_reviews=min_num_of_reviews, num=num, min_price=min_price, max_price=max_price)

        return self._dictfy(filtered_laptops)

    def _dictfy(self, laptops: list):
        dict_list = []
        for laptop in laptops:
            dict = {}
            dict['brand'] = laptop[0]
            dict['name'] = laptop[1]
            dict['price'] = laptop[2]
            dict['description'] = laptop[3]
            dict['num_reviews'] = laptop[4]
            dict['num_stars'] = laptop[5]
            dict['url'] = laptop[6]
            dict_list.append(dict)
        response = {}
        response['laptops'] = dict_list
        return response

    def close_browser(self):
        self.browser.close()

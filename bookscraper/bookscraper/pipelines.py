# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value:str = adapter.get(field_name)
                adapter[field_name] = value.strip()

        ## category & product type --> switch to lowercase
        lowercase_keys: list[str] = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value:str = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        ## price --> convert to float
        price_keys: list[str] = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value:str = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        ## availability --> extract number of books in stock
        availability_str: str = adapter.get('availability')
        split_str_arr = availability_str.split('(')
        if len(split_str_arr) != 2:
            adapter['availability'] = 0
        else:
            availability_split_arr = split_str_arr[1].split(' ')
            adapter['availability'] = int(availability_split_arr[0])

        ## num_reviews --> convert string to number
        num_reviews_str: str = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_str)

        ## stars --> convert text to number
        stars_str: str = adapter.get('stars')
        match stars_str.lower():
            case 'zero':
                adapter['stars'] = 0
            case 'one':
                adapter['stars'] = 1
            case 'two':
                adapter['stars'] = 2
            case 'three':
                adapter['stars'] = 3
            case 'four':
                adapter['stars'] = 4
            case 'five':
                adapter['stars'] = 5

        return item

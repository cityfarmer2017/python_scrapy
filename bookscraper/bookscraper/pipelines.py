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


import mysql.connector

class SaveToMySQLPipeline:
    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'books'
        )

        ## create cusor, used to execute commands
        self.cur = self.conn.cursor()

        ## create books table if none exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id int NOT NULL auto_increment,
                url VARCHAR(255),
                tittle text,
                product_type VARCHAR(255),
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                tax DECIMAL,
                price DECIMAL,
                availability INTEGER,
                num_reviews INTEGER,
                stars INTEGER,
                category VARCHAR(255),
                description text,
                PRIMARY KEY (id)
            )
        """)

    def process_item(self, item, spider):
        ## define insert statement
        self.cur.execute(""" insert into books (
                url,
                tittle,
                product_type,
                price_excl_tax,
                price_incl_tax,
                tax,
                price,
                availability,
                num_reviews,
                stars,
                category,
                description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )""", (
            item["url"],
            item["tittle"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
            str(item["description"][0])
        ))

        ## execute insert of data into database
        self.conn.commit()
        return item

    def close_spider(self, spider):
        ## close cursor & connection to database
        self.cur.close()
        self.conn.close()
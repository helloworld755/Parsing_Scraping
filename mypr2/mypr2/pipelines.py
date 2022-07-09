# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class Mypr2Pipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('mypr2.db')
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        create_query = '''
            CREATE TABLE IF NOT EXISTS mypr2(
                image TEXT,
                name TEXT,
                price TEXT,
                description TEXT
            )
        '''
        try:
            self.cursor.execute(create_query)
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

        save_query = '''
            INSERT INTO mypr2(
                image, name, price, description
            )
            VALUES (
                ?,
                ?,
                ?,
                ?
            )
        '''
        self.cursor.execute(save_query, (item.get('image'), item.get('name'), item.get('price'), item.get('description')))
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

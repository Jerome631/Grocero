import os
import psycopg2
from datetime import date
today = date.today()


PRICE_DAYS_BACK = 30
DB_PASS = os.getenv("DB_PASS", "Fortify136")


class DBConnector:

    def __init__(self):
        self._conn_string = f"host='grocerodb.cjy8c8kiefqe.eu-north-1.rds.amazonaws.com' dbname='postgres' user='Jerome' password='{DB_PASS}'"
        self._conn = psycopg2.connect(self._conn_string)
        self._cursor = self._conn.cursor()
        print(f"DB connection established, cursor assigned")

    def perform_insert(self, insert_data):
        """
        Method to insert the data and commit it.
        :param insert_data:
        :return:
        """
        print(f"Entered insert function")
        for item in insert_data:
            try:
                print(f"Inserting data")
                print(item)
                self._cursor.execute(item)
                self._conn.commit()
            except Exception as e:
                print(f"Insert failed")
                print(e)

    def get_item(self, item):
        try:
            select = f"select id,description,retailer,price,url,last_updated from product where category like '{item.lower()}' order by last_updated ASC limit (160);"
            self._cursor.execute(select)
            return self._cursor.fetchall()
        except Exception as e:
            print(e)


    def should_fetch_new(self, item):
        """

        Checks if data has been found within the past N days.

        :param item:
        :return:
        """
        select = f"select date_trunc('hour', last_updated),category from product WHERE date_trunc('hour', last_updated) >  NOW() - INTERVAL '{PRICE_DAYS_BACK} days' AND category ilike '{item}' limit(1);"
        self._cursor.execute(select)
        data = self._cursor.fetchall()

        # If there is no data returned by the cursor, that means we need to get some
        if data:
            print(f"There is data within {PRICE_DAYS_BACK} days")
            return False
        print(f"No data for {item} within past {PRICE_DAYS_BACK} days")
        return True

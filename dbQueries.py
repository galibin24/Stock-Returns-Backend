import psycopg2
import pandas.io.sql as sqlio
import time
import pandas

connection = psycopg2.connect(
    user="galibin24",
    password="Nn240494",
    host="127.0.0.1",
    port="5432",
    database="local_stocks",
)

cursor = connection.cursor()

# params = [date(range), cap ]
# cursor.execute(postgreSQL_select_Query)
# mobile_records = cursor.fetchall()

# TODO query to get data based on cap and date


class Query:
    def __init__(self, params):
        pass
        # self.cap = params.cap
        # self.dates = [self.get_time_stamps(params.date)]
        # self.change = params.change

    def get_time_stamps(self):
        pass

    def get_data(self):
        # query = """SELECT * FROM "Mega" WHERE datetime < 1577836800
        #     and datetime > 1483228800"""
        query = """ SELECT * FROM "Mega" 
                    WHERE datetime < 1577836800 
                        and datetime > 1483228800
                        
                        ORDER BY ticker asc, 
                                datetime asc """

        data = sqlio.read_sql_query(query, connection)
        return data


start = time.time()
makeQuery = Query({"cap": "hi"})
makeQuery.get_data()

# print(time.time() - start)
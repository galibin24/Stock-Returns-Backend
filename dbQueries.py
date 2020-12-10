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


class Query:
    def __init__(self, start_date, end_date, cap_type):
        self.start_date = start_date
        self.end_date = end_date
        self.cap_type = cap_type
        pass
        # self.cap = params.cap
        # self.dates = [self.get_time_stamps(params.date)]
        # self.change = params.change

    def get_time_stamps(self):
        pass

    def get_data(self):
        # query = """SELECT * FROM "Mega" WHERE datetime < 1577836800
        #     and datetime > 1483228800"""

        query = f'SELECT * FROM "{self.cap_type}" WHERE datetime < {self.end_date} and datetime > {self.start_date} ORDER BY ticker asc, datetime asc '
        print(query)
        data = sqlio.read_sql_query(query, connection)
        return data


# start = time.time()
# makeQuery = Query({"cap": "hi"})
# makeQuery.get_data()

# print(time.time() - start)
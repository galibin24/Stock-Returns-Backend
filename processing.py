from dbQueries import Query
import pandas as pd
import time


# TODO make sure cap_types in database match the frontend ones(VALIDATIORS)
# TODO do the the positive recovery
# TODO refactor for query to be entirly independent entity


class Processor:
    def __init__(self, params):
        # print(params)

        self.start_date = int(params["startDate"])
        self.end_date = int(params["endDate"])
        self.cap_type = params["marketCap"]
        self.percentage_drop = int(params["percentageDrop"]) / 100
        self.type_of_drop = params["typeOfDrop"]
        self.days_to_recover = int(params["daysToRecover"])
        print(self.percentage_drop)

        pass

    def process(self):
        if self.type_of_drop == "single":
            return self.process_single_day_negative()
        else:
            process_consecutive(params)

    # this for when stock dropped
    def process_single_day_negative(self):
        data = Query(self.start_date, self.end_date, self.cap_type).get_data()
        # print(data)
        # TODO more optimization here as well
        stock_tickers = pd.unique(data["ticker"].values)
        stock_dict = self.get_stocks_dict(stock_tickers)

        stock_droped = data.loc[data["day_drop"] <= self.percentage_drop]
        list_of_drops = stock_droped.index.tolist()
        # TODO see if I can replace this looping with native pandas(numpy) operation
        # TODO if no numpy option rewrite as generator expression(check if aplicable)
        for i in list_of_drops:
            recovery = i + self.days_to_recover + 1
            # get the range of recovery
            recovery_dates = data.iloc[i:recovery]
            # price it droped from(open price)
            start_price = recovery_dates.iloc[0, 1]
            print(start_price)
            # don't wanna compare to first day
            recovery_dates_no_first_day = recovery_dates.drop([i])
            # dataframes where price recovered()
            # TODO see if there more effiecient way
            recoveredDays = recovery_dates_no_first_day.loc[
                (recovery_dates["close_price"] >= start_price)
                | (recovery_dates["open_price"] >= start_price)
            ]
            # if dataframe with recovered prices not empty
            if not recoveredDays.empty:
                print("found one")
                days_to_recover = recoveredDays.index.values[0] - i
                # get the entry
                df_to_send = recovery_dates.iloc[[0]]
                df_to_send.insert(9, "days_to_recover", days_to_recover)
                df_to_dict = df_to_send.to_dict("index")
                ticker = df_to_send["ticker"].values[0]

                stock_dict[ticker].append(df_to_dict[i])

        # TODO can be but should be changed
        for i in stock_tickers:
            if not stock_dict[i]:
                stock_dict.pop(i)

        # print(stock_dict)
        return stock_dict

    def process_consecutive(self):

        pass

    def get_empty_df(self, columns):
        columns.append("days_to_recover")
        clean_df = pd.DataFrame(columns=columns)
        return clean_df

    def get_stocks_dict(self, stocks):
        stock_dict = {}
        for i in stocks:
            stock_dict[i] = []
        return stock_dict


# start = time.time()
# operator = Processor({"cap": "hi"})
# operator.process_single_day()
# print(time.time() - start)
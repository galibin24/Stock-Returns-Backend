from dbQueries import Query
import pandas as pd
import time


class Processor:
    def __init__(self, params):
        self.params = params
        self.recovery_limit = 4
        pass

    def process(self):
        if params.type == "single":
            process_single_day(params)
        else:
            process_consecutive(params)

    def process_single_day(self):
        data = Query(self.params).get_data()
        stock_dict = self.get_stocks_dict(pd.unique(data["ticker"].values))

        stock_droped = data.loc[data["day_drop"] <= -0.01]
        list_of_drops = stock_droped.index.tolist()
        # TODO see if I can replace this looping with native pandas(numpy) operation
        # TODO if no numpy option rewrite as generator expression(check if aplicable)
        for i in list_of_drops:
            recovery = i + self.recovery_limit + 1
            # get the range of recovery
            recovery_dates = data.iloc[i:recovery]
            # price it droped from(open price)
            start_price = recovery_dates.iloc[0, 2]
            # dataframes where price recovered()
            # TODO see if there more effiecient way
            recoveredDays = recovery_dates.loc[
                recovery_dates["close_price"] >= start_price
            ]
            # if dataframe with recovered prices not empty
            if not recoveredDays.empty:
                days_to_recover = recoveredDays.index.values[0] - i
                # get the entry
                df_to_send = recovery_dates.iloc[[0]]
                df_to_send.insert(8, "days_to_recover", days_to_recover)
                df_to_dict = df_to_send.to_dict("index")
                ticker = df_to_send["ticker"].values[0]

                stock_dict[ticker].append(df_to_dict[i])

        print(stock_dict)
        pass

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


start = time.time()
operator = Processor({"cap": "hi"})
operator.process_single_day()
print(time.time() - start)
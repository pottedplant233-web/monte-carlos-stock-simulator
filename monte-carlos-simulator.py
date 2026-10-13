from stocks import GetData
from stocks import sandp
from stocks import percent_performance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

class Stock: #does calculations nshit with numpy
    def __init__(self, closing, volatility, mean_return, ticker):
        self.closing = closing
        self.volatility = volatility
        self.mean_return = mean_return
        self.ticker = ticker
    def simulate(self):
        simulations = {}
        for i in range(1000):
            simulated_returns = np.random.normal(self.mean_return, self.volatility, 252)
            simulations[f'simulation{i}'] = simulated_returns
        df = pd.DataFrame(simulations)
        df.to_csv(f'{self.ticker}simulatedreturns.csv', index=False)
    def convert(self):
        return_data = pd.read_csv(f'{self.ticker}simulatedreturns.csv')
        converted_returns = {}
        for i in range(return_data.shape[1]):
            converted_array = [self.closing]
            array = np.array(return_data[f'simulation{i}'])
            for index, value in enumerate(array):
                    converted_array.append(converted_array[-1] * (1 + array[index]))
            converted_returns[i] = converted_array

        df_two = pd.DataFrame(converted_returns)
        df_two.to_csv(f'{self.ticker}converted.csv', index=False)
    def get_time_steps(self):
        df_three = pd.read_csv(f'{self.ticker}converted.csv')
        return len(df_three)


def main():
    tick_request = input('ticker:').upper().strip()
    getter = GetData(tick_request)
    getter.get_ticker()
    stock_data = getter.get_data()
    closing_price = stock_data.iloc[-1]['Close']

    volatility = getter.volatility() / 100
    daily_return = getter.daily_return() / 100
    mean_return = np.mean(daily_return)

    monte = Stock(closing_price, volatility, mean_return, tick_request)
    monte.simulate()
    monte.convert()
    time_steps = monte.get_time_steps()


    trading_days = np.arange(0, time_steps)
    plot_carlo(trading_days, tick_request, time_steps)
    plot_hist(trading_days, tick_request, time_steps)

def plot_carlo(trading_days, tick_request, time_steps):
    converted_df = pd.read_csv(f'{tick_request}converted.csv')
    for column in converted_df:
        plt.plot(trading_days, converted_df[column])

    plt.title(f'monte carlo simulation of 1000 {tick_request} outcomes')
    plt.xticks(labels=trading_days[0:time_steps:10],
               ticks=np.arange(0, time_steps, 10),
               rotation= 45,
               fontsize=8
               )
    plt.xlabel('Trading Days')
    plt.ylabel('USD')
    plt.grid()
    plt.show()

def plot_hist(trading_days, tick_request, time_steps):
    last_data = pd.read_csv(f'{tick_request}converted.csv')
    final_prices = last_data.iloc[-1]
    plt.hist(final_prices, bins=32)

    plt.xlabel('Final Simulated Price USD')
    plt.ylabel('Frequency')
    plt.title('histogram of final price')
    plt.show()



if __name__ == '__main__':
    main()
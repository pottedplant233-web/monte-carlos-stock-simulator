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
        df.to_csv(f'{self.ticker}simulatedreturns.csv')
    def convert(self):
        return_data = pd.read_csv(f'{self.ticker}simulatedreturns.csv')
        converted_returns = {}
        for i in range(return_data.shape[1]):
            converted_array = []
            array = np.array(return_data[f'simulation{i}'])
            for index, value in enumerate(array):
                if index == 0:
                    converted_array.append(self.closing)
                else:
                    converted_array.append(converted_array[index-1] * (1 + array[index]))
            converted_returns[i] = converted_array

        df_two = pd.DataFrame(converted_returns)
        df_two.to_csv(f'{self.ticker}converted.csv')

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





if __name__ == '__main__':
    main()
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from matplotlib import style
import pandas
from pandas import DataFrame
import csv

#ts = TimeSeries(key='TK8VW7JEPYHWNMA0', output_format='pandas')
style.use('ggplot')
#data, meta_data = ts.get_intraday(symbol='SPX',interval='15min',outputsize='full')
#df = DataFrame(data)
#df.to_csv('stock data.csv')
data = pandas.read_csv('stock data.csv', parse_dates=True, index_col=0)


data['4. close'].plot()
data['100ma'] = data['4. close'].rolling(window=10, min_periods= 0).mean()
data['100ma'].plot()
plt.title('S&P 500 CHART (5 min)')
plt.show()




#libraries import

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# graph function
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

# yfinance to extract stock data

tesla = yf.Ticker('TSLA')
tesla_data = tesla.history(period='1d', start='2022-12-22', end='2022-12-30')
tesla_data.reset_index(inplace=True)
print(tesla_data.head().to_string())

# webscrapping method to extract tesla revenue data

url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
html_data = requests.get(url).text

soup = BeautifulSoup(html_data,"html5lib")

tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if ('Tesla Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')

        for row in rows:
            col = row.find_all('td')

            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',', '').replace('$', '')

                tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index=True)

tesla_revenue
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'].astype(bool)]
print(tesla_revenue.tail())

# yfinance data to extract gme stock data

gme = yf.Ticker('GME')
gme_data = gme.history(period='1d', start='2022-12-22', end='2022-12-30')
gme_data.reset_index(inplace=True)
print(gme_data.head().to_string())

# webscrapping to extract GME Revenue data

url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
html_data = requests.get(url).text
soup = BeautifulSoup(html_data,"html5lib")

gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if ('GameStop Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')

        for row in rows:
            col = row.find_all('td')

            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',', '').replace('$', '')

                gme_revenue = gme_revenue.append({"Date": date, "Revenue": revenue}, ignore_index=True)

print(gme_revenue.tail())




# plot tesla graph

make_graph(tesla_data[['Date','Close']], tesla_revenue, 'Tesla')

# plot gamestop graph

make_graph(gme_data[['Date','Close']], gme_revenue, 'GameStop')



#!/usr/bin/env python
# coding: utf-8

# In[5]:


get_ipython().system('python -m pip install yfinance')
get_ipython().system('python -m pip install pandas')
get_ipython().system('python -m pip install requests')
get_ipython().system('python -m pip install bs4')
get_ipython().system('python -m pip install plotly')


# In[6]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[7]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# # Question 1

# In[8]:


tesla = yf.Ticker("TSLA")


# In[9]:


tesla_data = tesla.history(period="max")


# In[10]:


tesla_data.reset_index(inplace= True)
tesla_data.head()


# # Question 2

# In[11]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text


# In[12]:


soup = BeautifulSoup(html_data, "html5lib")
print(soup.prettify())


# In[13]:


tesla_revenue = pd.DataFrame(columns = ["Date","Revenue"])

for table in soup.find_all('table'):
    if table.find('th').getText().startswith("Tesla Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            tesla_revenue = tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[14]:


tesla_revenue.dropna(axis=0, how='all', subset=['Revenue']) 
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[15]:


tesla_revenue.tail(5)


# # Question 3

# In[16]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[17]:


gme = yf.Ticker('GME')


# In[18]:


gme_data = gme.history(period = "max")


# In[19]:


gme_data.reset_index(inplace=True)
gme_data.head(5)


# # Question 4

# In[20]:


url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text


# In[21]:


soup = BeautifulSoup(html_data, "html5lib")
print(soup.prettify())


# In[22]:


gme_revenue = pd.DataFrame(columns = ["Date","Revenue"])

for table in soup.find_all('table'):
    if table.find('th').getText().startswith("GameStop Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[23]:


gme_revenue.tail(5)


# # Question 5

# In[24]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# # Question 6

# In[25]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:





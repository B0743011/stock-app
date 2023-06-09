# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aUPNrDIlWRVVrZO5x8zcX5LPdxxp6OPp
"""

!pip install streamlit

import streamlit as st
import pandas as pd
# https://www.twse.com.tw/zh/page/products/stock-code2.html
# TAI_TWO_ind="https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"

TAI_ind='https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
# data encoded in Traditional Chinese, 資料使用繁體中文編碼
df=pd.read_html(TAI_ind,encoding='cp950')
# the data in the first page (table)
# only the first feature, 有價證券代號及名稱, we want, 
df[0]
# df[0][0][2:]
#   first table, 第一個表格
#      feature 0, 欄位 0
#         start from third rows, i.e. 2

df[0][0][2:].values
# extract data and split by '\u3000', 利用字元 '\u3000' 將每一個欄位分成兩個, 
# create two-column DataFrame, 
data = df[0][0][2:].str.split('\u3000', n=1, expand=True)

# create two-column DataFrame, 將上述的兩個公開的資料成為新的欄位
df1 = pd.DataFrame({'Symbol': data[0], 'Name': data[1]})

# convert ticker to yahoo tick,  將上市公司的代碼變成 yahoo 代碼
df1['Symbol'] = df1['Symbol'].apply(lambda x: x + '.TW')
df1.head()
# remove any null value in cell, 去掉沒資料的欄位
df1.fillna('', inplace=True)

# and save to a file, used in later, 並存成檔案供日後使用
df1.to_csv("TWSE_TW-1.csv",index=False)

df1=pd.read_csv("TWSE_TW-1.csv",index_col=0)
df1.fillna('', inplace=True)
# set up Streamlit app
st.title("TWSE Stock Search, 台灣股票代號查詢")

# add search box and dropdown
search_term = st.text_input("Enter search term, 輸入查詢資料:")
search_by = st.selectbox("Search by column:", options=['公司代碼', '公司名稱'])

# search for matching rows
if search_term:
    if search_by == 'Symbol':
        result = df1[df1['Symbol'].str.contains(search_term)]
    elif search_by == 'Name':
        result = df1[df1['Name'].str.contains(search_term)]
    else:
        result = pd.DataFrame()
    st.write(result)

"""2/21 B0743011 詹恩睿

"""
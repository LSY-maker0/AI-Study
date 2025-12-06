# 可以从第三方联网获取股票数据

stocks={
  'AAPL':191.88,
  'GOOD':728,
  'IBM':23,
  'FB':123,
}

# new_stocks={key:value for key,value in stocks.items() if value>100}
# print(new_stocks)

# zip变成二元组
# dict1=dict(zip(stocks.values(),stocks.keys()))
# print(dict1)

# 获取最大的股票名称
# print(max(zip(stocks.values(),stocks.keys()))[1])
# _,max_code=max(zip(stocks.values(),stocks.keys()))
# print(max_code)

# print(max(stocks,key=stocks.get))

# 股票价格从高到底排序
print(sorted(stocks,key=stocks.get,reverse=True))
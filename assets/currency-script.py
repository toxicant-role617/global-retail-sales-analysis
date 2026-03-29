import pandas as pd
from io import StringIO

data = """Exchange ID;ExchangeRate;Exchange Currency
1;1.0;USD
2;0.75;GBP
3;0.85;EUR
4;3.67;AED
5;1.3;AUD"""

df = pd.read_csv(StringIO(data), sep=';')

print(df)

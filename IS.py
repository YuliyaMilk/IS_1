import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot

table = pd.read_table('https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv')

#1.Вывести: кол-во наблюдений в датасете
print('1.Вывести: кол-во наблюдений в датасете: ', table.shape[0])

#2.Вывести названия столбцов
print('2.Вывести названия столбцов: ', table.columns.tolist())

#3.Определить самую частую позицию (item) в заказе 
print('3.Определить самую частую позицию (item) в заказе: ', table.mode()['item_name'][0])
order = table.groupby('item_name')['quantity'].sum()
print('3.Определить самую частую позицию (item) в заказе: ',  table.groupby('item_name')['quantity'].sum().idxmax(), ' - ',table.groupby('item_name')['quantity'].sum().max() )


#4. Построить гистрограмму частоты заказов по позициям (item)
print('4. Построить гистрограмму частоты заказов по позициям (item): ', order.hist())
print(order)
sns.histplot(order["item_name"], binwidth=0.05)
pyplot.show()
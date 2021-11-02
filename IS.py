import pandas as pd
from matplotlib import pyplot
from currency_converter import CurrencyConverter

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
print('4. Построить гистрограмму частоты заказов по позициям (item): ')
order.plot(kind='bar')
pyplot.xlabel('Позиция')
pyplot.ylabel('Частота заказов')
pyplot.title('Частота заказов по позициям')
#pyplot.show()

#5. Измените тип переменной item_price c с помощью лямбды функции
#fun=lambda x:float(x[1:-1])
fun=lambda x:float(x.strip('$'))
table['item_price'] = table['item_price'].apply(fun)
print('5. Измените тип переменной item_price c с помощью лямбды функции: ')
print(table.head())

#6. Построить гистограмму кол-во денег заработанных по каждой позиции (item)
print('6. Построить гистограмму кол-во денег заработанных по каждой позиции (item): ')
item_price = pd.to_numeric(table['item_price'])
quantity = pd.to_numeric(table['quantity'])

table['total_price'] = quantity* item_price
table.groupby('item_name')['total_price'].sum().plot(kind='bar')
pyplot.xlabel('Позиция')
pyplot.ylabel('Количество денег')
pyplot.title('Количество денег заработанных по каждой позиции')
#pyplot.show()

#7. Средняя сумма заказа? (минимум 2 способа)
print('7. Средняя сумма заказа?: ')

total_order_sum = table['total_price'].sum()
num_orders = len(set(table['order_id']))
average_order_price = round(total_order_sum / num_orders, 2)  
print('1 способ:', average_order_price)

print('2 способ:', round(table.groupby('order_id')['total_price'].sum().mean(), 2))

#8. Выведите среднее, минимальное и максимальное, медианное значения позиций в заказе
num_uniq_item = table['item_name'].value_counts().shape[0]
num_item = table['quantity'].sum()
print('8. Выведите среднее, минимальное и максимальное, медианное значения позиций в заказе: ')

print('Среднее = ', round(table['quantity'].sum() / num_orders, 2))
print('Минимальное = ', table.groupby('order_id')['quantity'].sum().min())
print('Максимальное = ', table.groupby('order_id')['quantity'].sum().max())
print('Медианное = ', table.groupby('order_id')['quantity'].sum().median())

#9. Определить статистику заказов стейков, а также статистику заказов прожарки.

#10. Добавить новый столбец цен на каждую позицию в заказе в рублях.
print('10. Добавить новый столбец цен на каждую позицию в заказе в рублях: ')
c = CurrencyConverter()
fun1=lambda x:(str(round((c.convert(pd.to_numeric(x), 'USD', 'RUB')), 2))+' RUB')
table['price_rubles'] = table['item_price'].apply(fun1)
print(table)

#11. Сгруппировать заказы по входящим позициям в него. Отдельно сгруппировать по стейкам во всех видах прожарках.
#12. Определить цену по каждой позиции в отдельности. 





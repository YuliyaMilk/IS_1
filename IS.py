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
print('9. Определить статистику заказов стейков, а также статистику заказов прожарки: ')
item_tot = table[table['item_name'].str.contains('Steak')].groupby(['item_name']).agg({"total_price": "mean", "quantity": "count", "order_id": "count"}).reset_index()
item_tot = item_tot.rename(
    columns={"total_price": "avg_price_paid", "order_id": "times_ordered"}
)
print(item_tot)

item_tot = table['choice_description'].str.split(expand=True).stack().reset_index(level=1, drop=True).to_frame('roasting').merge(table, left_index=True, right_index=True)
item_tot = item_tot[item_tot['roasting'].str.contains('Mild|Medium|Hot')]
item_tot['roasting'] = item_tot.roasting.str.strip(',[]()')
item_tot = item_tot.groupby(['roasting']).agg({"quantity": "count", "order_id": "count"}).reset_index()
print(item_tot)

#10. Добавить новый столбец цен на каждую позицию в заказе в рублях.
print('10. Добавить новый столбец цен на каждую позицию в заказе в рублях: ')
c = CurrencyConverter()
fun1=lambda x:(str(round((c.convert(pd.to_numeric(x), 'USD', 'RUB')), 2))+' RUB')
table['price_rubles'] = table['item_price'].apply(fun1)
print(table)

#11. Сгруппировать заказы по входящим позициям в него. Отдельно сгруппировать по стейкам во всех видах прожарках.
print('11. Сгруппировать заказы по входящим позициям в него. Отдельно сгруппировать по стейкам во всех видах прожарках: ')

group_order = pd.DataFrame(
    table.groupby(['item_name', 'order_id'])
    .agg({"total_price": "mean", "quantity": "count"})
)
print(group_order)

#item_tot = table[table['item_name'].str.contains('Steak')].groupby(['item_name', 'choice_description','order_id']).sum().reset_index()
item_tot = table['choice_description'].str.split(expand=True).stack().reset_index(level=1, drop=True).to_frame('roasting').merge(table, left_index=True, right_index=True)
item_tot = item_tot[item_tot['roasting'].str.contains('Mild|Medium|Hot')]
item_tot['roasting'] = item_tot.roasting.str.strip(',[]()')
item_tot = item_tot[item_tot['item_name'].str.contains('Steak')].groupby(['roasting', 'order_id', 'item_name', 'choice_description']).agg({"total_price": "mean", "quantity": "count"})
print(item_tot)


#12. Определить цену по каждой позиции в отдельности. 
print('12. Определить цену по каждой позиции в отдельности: ')

by_item = pd.DataFrame(
    table.groupby("item_name")
    .agg({"total_price": "mean", "quantity": "count"})
    .reset_index()
)
by_item = by_item.rename(
    columns={"total_price": "avg_price_paid", "quantity": "times_ordered"}
)

by_item["revenue"] = by_item["avg_price_paid"] * by_item["times_ordered"]

print(by_item)

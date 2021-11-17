import pandas as pd
from matplotlib import pyplot
import seaborn as sns
import umap

table = pd.read_table('https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv')
fun=lambda x:float(x.strip('$'))
table['item_price'] = table['item_price'].apply(fun)
distinct_items = table.describe(include='all').loc['unique', :]
print(distinct_items)

embedding = umap.UMAP(n_neighbors=5).fit_transform(table.drop(['choice_description','item_name'], axis=1)) # преобразовываем

pyplot.scatter(
    embedding[:, 0],
    embedding[:, 1],
    c=[sns.color_palette()[x] for x in table.item_name.map()])
pyplot.gca().set_aspect('equal', 'datalim')
pyplot.title('UMAP projection of the Penguin dataset', fontsize=24)
pyplot.show()
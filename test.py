import RandomInventoryTable as rit
import pandas as pd

dict = {
    'a':[1,3,4,5, 10, 25, 64],
    'b':[1,3,4,5, 10, 25, 64]
    }

df = pd.DataFrame(dict)

table = rit.RandomInventory(df=df, col_name_total_value='a')

table._sqrt_column('a', 'd')

print(table.df)
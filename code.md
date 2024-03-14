## Importing libraries
``` Python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
np.set_printoptions(suppress = True, linewidth = 100, precision =2)
```
## Importing the database 
``` Python
df = pd.read_excel('Online Retail.xlsx')
```
## Reviewing the data
``` Python
df.head()
df.tail()
```
## Removing duplicates and saving it in 'dfc'
``` Python
dfc = df.copy().drop_duplicates()
```
## Reviewing data again
``` Python
dfc.shape ##Checking data shape
dfc.info() ## checking data type
dfc.isnull().sum() ## checking for null values
dfc.nunique() ## checking for no. of unique values
dfc.describe() ## statistics of data
```
#### The column "Description" and "CustomerID" have missing data.
#### The no. of unique "StockCode" and "Description" are different which need attention.
#### The minimum value of Quantity is negative which is not possible,also the price of a product can't be negative.
## Checking for negative quantity
``` Python
print(dfc[dfc['Quantity'] < 0])
```
#### There are 10,624 rows containing negative values, which could significantly impact the analysis. Additionally, these values correspond to Invoice numbers starting with "C"
#### Investigating the connection between negative quantities and Invoice numbers that start with "C".
``` Python
print(dfc[dfc['Quantity'] < 0 & dfc['InvoiceNo'].astype(str).str.contains('C')])
```
#### Indeed, the presence of "C" in the Invoice numbers for rows with negative Quantity suggests that these orders may have been either cancelled or returned.
## Checking for products if listed with negative price.
``` Python
print(dfc[dfc['UnitPrice'] < 0])
```
#### There are two products with a negative price, and their Invoice numbers begin with "A".
#### Verifying whether there are additional Invoice numbers that begin with "A".
``` Python
print(dfc[dfc['InvoiceNo'].astype(str).str.contains('A')])
```
#### There are a total of three Invoice IDs that contain the letter "A".
#### Since the price of a product cannot be negative, we will proceed to remove these rows.
``` Python
dfc = dfc[dfc['UnitPrice'] >= 0].copy()
```
#### There are numerous missing values in the CustomerID column. We will replace these with "Unknown".
``` Python
dfc['CustomerID'].replace(np.nan,"Unknown", inplace=True)
dfc.CustomerID.isnull().sum()
```
## Handling the "Description" column.
#### There are 1,454 rows with null values. We can proceed to delete these rows.
``` Python
dfc = dfc.dropna(subset=['Description'])
```
## Column "Invoice Date"
#### We will extract the month and day from this column and place them into two new separate columns.And then we will delete this column.
``` Python
dfc['InvoiceDate'] = pd.to_datetime(dfc['InvoiceDate'])
dfc['Purchase_Month'] = dfc['InvoiceDate'].dt.strftime('%Y-%m')
dfc['Day_of_Purchase']= dfc['InvoiceDate'].dt.day_name()
print(dfc['Day_of_Purchase'].unique())
dfc = dfc.drop(columns=['InvoiceDate'])
```
## Checking if there are any remaining null values.
``` Python
dfc.isnull().sum()
```
## Checking for outliners
#### Column "UnitPrice"
``` Python
import matplotlib.pyplot as plt
import seaborn as sns
sns.boxplot(x=dfc['UnitPrice'])
plt.title('Boxplot of UnitPrice')
plt.show()
```
#### There are a few outliers, but it's acceptable to have them since the price can vary from product to product.
#### Column "Quantity"
``` Python
plt.scatter(dfc.index, dfc['Quantity'])
plt.title('Scatter plot of Quantity')
plt.xlabel('Index')
plt.ylabel('Quantity')
plt.show()
```
#### There are a few outliers, but it's acceptable to have them since the quantity can vary based on customer demand.
## Dropping any remaining duplicates and saving the dataset.
``` Python
dfc= dfc.copy().drop_duplicates()
dfc.to_csv('Online_Retail_Cleaned.csv', index=False)
```
## Analyzing the data to derive meaningful insights.
#### Separate the data into two parts: can_order (cancelled orders) and suc_order (successful orders).
#### Data of successful sales.
``` Python
suc_data = dfc[~dfc['InvoiceNo'].str.contains('C', na=False)].copy()
suc_data
```
#### Data of cancelled or returned products.
``` Python
can_data = dfc[dfc['InvoiceNo'].str.contains('C', na=False)].copy()
can_data
```
### Sales trend
#### Are there any seasonal patterns or trends in sales? Which  days of the week or month have the highest sales?
``` Python
sales_over_time= suc_data.groupby(['Purchase_Month']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
print(sales_over_time.sort_values(ascending=False))

plt.figure(figsize=(10, 6))
sns.lineplot(data=sales_over_time, marker='o')
plt.title('Sales Amount Per Month')
plt.xlabel('Sales Month')
plt.ylabel('Sales Amount')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
```

``` Python

```

``` Python

```

``` Python

```

``` Python

```

``` Python

```

``` Python

```





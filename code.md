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
#### Over Month
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
![image](https://github.com/him100gupta/Online-Retail-Exploratory-Data-Analysis-with-Python/assets/29143253/8bc66da6-132c-4e40-ba60-424d5689adfc)
#### Over Days
``` Python
sales_over_week= suc_data.groupby(['Day_of_Purchase']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
sales_over_week.sort_values( ascending=False).head(5)

plt.figure(figsize=(10, 6))
sns.barplot(x=sales_over_week.index, y=sales_over_week.values)

for i, value in enumerate(sales_over_week.values):
    plt.plot(i, value, 'o', color='black', zorder=3)

plt.title('Sales Amount Over Days')
plt.xlabel('Day')
plt.ylabel('Total Sales')
plt.grid(True)
plt.xticks(rotation=45)
plt.show()
```
![image](https://github.com/him100gupta/Model-Car-Database-Analysis-using-MySQL-Workbench/assets/29143253/0a23c742-28d4-4167-a53b-a164edbb4f27)
### Product performance
#### Which are the best-selling products?
``` Python
product_sales = suc_data.groupby(['StockCode', 'Description']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
product_sales.sort_values( ascending=False).head(10)
```
#### which are the trending products each month. 
``` Python
Trending_products = suc_data.groupby([ 'Purchase_Month', 'StockCode','Description'])['Quantity'].sum().reset_index()
Trending_products['Rank'] = Trending_products.groupby(['Purchase_Month'])['Quantity'].rank(ascending=False, method='dense')
Top_5_products_per_month = Trending_products[Trending_products['Rank'] <= 5]
Top_5_products_per_month
```
### Customer Behaviour
#### Who are the most valuable customers in terms of total spending or frequency of purchases?
``` Python
customer_spending = suc_data.groupby('CustomerID')[['Quantity', 'UnitPrice']].sum()
customer_spending['total_spending'] = suc_data.groupby(['CustomerID']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
customer_spending_ranked = customer_spending.sort_values(by='total_spending', ascending=False)

customer_frequency = suc_data.groupby('CustomerID')['InvoiceNo'].nunique()
customer_frequency_ranked = customer_frequency.sort_values( ascending=False)

print("Top Customers by Total Spending:")
print(customer_spending_ranked.head(10))
print("\nTop Customers by Frequency of Purchases:")
print(customer_frequency_ranked.head(10))
```
#### What is the average order size? Are there any differences in purchasing behavior between new and returning customers?
``` Python
average_order_size = suc_data['Quantity'].sum() / suc_data['InvoiceNo'].nunique()
print("Average Order Size:", average_order_size)

customer_purchase_counts = suc_data.groupby('CustomerID')['InvoiceNo'].nunique()
new_customers = customer_purchase_counts[customer_purchase_counts == 1].index
returning_customers = customer_purchase_counts[customer_purchase_counts > 1].index

average_order_size_new = suc_data[suc_data['CustomerID'].isin(new_customers)]['Quantity'].sum() / len(new_customers)
average_order_size_returning = suc_data[suc_data['CustomerID'].isin(returning_customers)]['Quantity'].sum() / len(returning_customers)

print("Average Order Size for New Customers:", average_order_size_new)
print("Average Order Size for Returning Customers:", average_order_size_returning)
```
### Geographic Analysis
#### How do sales vary across different regions or countries?
``` Python
country_spending = suc_data.groupby('Country')[['Quantity', 'UnitPrice']].sum()
country_spending['Total_spending'] = suc_data.groupby(['Country']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
country_spending_ranked = country_spending.sort_values(by='Total_spending', ascending=False)

country_frequency = suc_data.groupby('Country')['InvoiceNo'].nunique()
country_frequency_ranked = country_frequency.sort_values( ascending=False)

print("Top countries by Total Spending:")
print(country_spending_ranked.head(10))
print("\nTop countries by Frequency of Purchases:")
print(country_frequency_ranked.head(10))
```
### Customer Retention
#### What is the overall customer retention rate, and how frequently do customers return to shop again?
#### Calculated the retention rate based only on customers whose CustomerID is known.
``` Python
ret_data = suc_data[suc_data['CustomerID'] != 'Unknown']
retention_rates = ret_data.groupby('Purchase_Month')['CustomerID'].apply(lambda x: len(set(x)) / len(set(ret_data['CustomerID'])))
print(retention_rates)

plt.figure(figsize=(10, 6))
sns.lineplot(data=retention_rates, marker='o')
plt.title('Retention Rates by Cohort')
plt.xlabel('Purchase Month')
plt.ylabel('Retention Rate')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()                                                               
```
![image](https://github.com/him100gupta/Model-Car-Database-Analysis-using-MySQL-Workbench/assets/29143253/11eb1145-a1dc-4a97-a7f3-27790e855937)
### Price analysis
#### What is the distribution of unit prices for products?
``` Python

unit_price_stats = suc_data['UnitPrice'].describe()
print("Summary Statistics of Unit Prices:")
print(unit_price_stats)
unit_price_frequency = suc_data['UnitPrice'].value_counts()

plt.figure(figsize=(10, 6))
plt.scatter(unit_price_frequency.index, unit_price_frequency.values, alpha=0.5)
plt.title('Price Distribution')
plt.xlabel('UnitPrice')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
```
![image](https://github.com/him100gupta/Model-Car-Database-Analysis-using-MySQL-Workbench/assets/29143253/3224e4d2-adc9-4ed4-b756-bd856ad9a563)
## Analyzing cancelled orders and it's impact.
#### what's the impact of cancelled orders on overall sales?
``` Python
total_cancelled_amount = (can_data['UnitPrice'] * can_data['Quantity']).sum()
print("Overall loss: ",total_cancelled_amount)
```
#### Comparision of successful orders and cancelled orders
``` Python
Can_per_month = can_data.groupby('Purchase_Month')['InvoiceNo'].nunique()
sales_per_month = suc_data.groupby('Purchase_Month')['InvoiceNo'].nunique()

plt.figure(figsize=(10, 6))
plt.plot(Can_per_month.index, Can_per_month.values, label='Cancelled Orders',marker='o')
plt.plot(sales_per_month.index, sales_per_month.values, label='Successful Sales', marker='o')
plt.xlabel('Month')
plt.ylabel('Number Of Orders')
plt.xticks(rotation=45)
plt.title('Comparision Of Successful Orders And Cancelled Orders Per Month')
plt.legend()
plt.grid(True)
plt.show()
```
![image](https://github.com/him100gupta/Model-Car-Database-Analysis-using-MySQL-Workbench/assets/29143253/80f63061-f9d5-4169-9de2-0785cc53415d)
#### How have cancelled orders impacted sales over the months?
``` Python
can_over_time= can_data.groupby(['Purchase_Month']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
print(can_over_time)

df1 = pd.DataFrame(sales_over_time)
df2 = pd.DataFrame(can_over_time)
df3 = df1 - df2

plt.figure(figsize=(10, 6))
plt.plot(df1.index, df1.values, label='Actual Sales',marker='o')
plt.plot(df3.index, df3.values, label='Expected Sales', marker='o')
plt.xlabel('Month')
plt.ylabel('Sales Amount')
plt.xticks(rotation=45)
plt.title('Comparision Of Expected Sales Amount And Actual Sales Amount Per Month')
plt.grid(True)
plt.legend()
plt.show()
```
![image](https://github.com/him100gupta/Model-Car-Database-Analysis-using-MySQL-Workbench/assets/29143253/cb4087e7-8362-4447-9a14-70262deccd4c)
#### How does the number of cancelled orders vary by day, and what patterns or trends can be identified from this data?
``` Python
Can_per_week = can_data.groupby('Day_of_Purchase')['InvoiceNo'].nunique()
print(Can_per_week)

plt.figure(figsize=(10, 6))
sns.barplot(x=Can_per_week.index, y=Can_per_week.values)
for i, value in enumerate(Can_per_week.values):
    plt.plot(i, value, 'o', color='black')

plt.title('Cancellation Per Day')
plt.xlabel('Cancellation Day')
plt.ylabel('No. of cancellation')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
```
![image](https://github.com/him100gupta/Model-Car-Database-Analysis-using-MySQL-Workbench/assets/29143253/c3804900-1b73-4636-ad6e-b0e764058979)
#### Which country's customers have the highest number of cancelled orders?
``` Python
Can_per_country = can_data.groupby('Country')['InvoiceNo'].nunique()
Can_per_country1 = Can_per_country.sort_values( ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=Can_per_country1.index, y=Can_per_country1.values)
plt.xlabel('Country')
plt.ylabel('Number of Cancelled Orders')
plt.title('Cancelled Orders per Country')
plt.xticks(rotation=90)
plt.show()
```
![image](https://github.com/him100gupta/Model-Car-Database-Analysis-using-MySQL-Workbench/assets/29143253/45efcffa-c7cf-4ae2-9d75-1bb33647ab33)
### Correlation
``` Python
numeric_df = suc_data.select_dtypes(include='number')
numeric_df['Total_price'] = numeric_df['Quantity'] * numeric_df['UnitPrice']
correlation_matrix = numeric_df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()
```
![image](https://github.com/him100gupta/Model-Car-Database-Analysis-using-MySQL-Workbench/assets/29143253/7fe9f3cd-86a5-49de-acd9-fa1c7d75c17d)



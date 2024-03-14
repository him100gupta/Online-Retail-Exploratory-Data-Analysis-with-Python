#!/usr/bin/env python
# coding: utf-8

# # Portfolio Project: Online Retail Exploratory Data Analysis with Python

# ## Overview
# 
# In this project, you will step into the shoes of an entry-level data analyst at an online retail company, helping interpret real-world data to help make a key business decision.

# ## Case Study
# In this project, you will be working with transactional data from an online retail store. The dataset contains information about customer purchases, including product details, quantities, prices, and timestamps. Your task is to explore and analyze this dataset to gain insights into the store's sales trends, customer behavior, and popular products. 
# 
# By conducting exploratory data analysis, you will identify patterns, outliers, and correlations in the data, allowing you to make data-driven decisions and recommendations to optimize the store's operations and improve customer satisfaction. Through visualizations and statistical analysis, you will uncover key trends, such as the busiest sales months, best-selling products, and the store's most valuable customers. Ultimately, this project aims to provide actionable insights that can drive strategic business decisions and enhance the store's overall performance in the competitive online retail market.

# ## Project Objectives
# 1. Describe data to answer key questions to uncover insights
# 2. Gain valuable insights that will help improve online retail performance
# 3. Provide analytic insights and data-driven recommendations

# ## Dataset
# 
# The dataset you will be working with is the "Online Retail" dataset. It contains transactional data of an online retail store from 2010 to 2011. The dataset is available as a .xlsx file named `Online Retail.xlsx`. This data file is already included in the Coursera Jupyter Notebook environment, however if you are working off-platform it can also be downloaded [here](https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx).
# 
# The dataset contains the following columns:
# 
# - InvoiceNo: Invoice number of the transaction
# - StockCode: Unique code of the product
# - Description: Description of the product
# - Quantity: Quantity of the product in the transaction
# - InvoiceDate: Date and time of the transaction
# - UnitPrice: Unit price of the product
# - CustomerID: Unique identifier of the customer
# - Country: Country where the transaction occurred

# ## Tasks
# 
# You may explore this dataset in any way you would like - however if you'd like some help getting started, here are a few ideas:
# 
# 1. Load the dataset into a Pandas DataFrame and display the first few rows to get an overview of the data.
# 2. Perform data cleaning by handling missing values, if any, and removing any redundant or unnecessary columns.
# 3. Explore the basic statistics of the dataset, including measures of central tendency and dispersion.
# 4. Perform data visualization to gain insights into the dataset. Generate appropriate plots, such as histograms, scatter plots, or bar plots, to visualize different aspects of the data.
# 5. Analyze the sales trends over time. Identify the busiest months and days of the week in terms of sales.
# 6. Explore the top-selling products and countries based on the quantity sold.
# 7. Identify any outliers or anomalies in the dataset and discuss their potential impact on the analysis.
# 8. Draw conclusions and summarize your findings from the exploratory data analysis.

# ## Task 1: Load the Data

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
np.set_printoptions(suppress = True, linewidth = 100, precision =2)


# In[3]:


df = pd.read_excel('Online Retail.xlsx')


# In[4]:


df.head()


# In[5]:


df.tail()


# #### we will start with dropping duplicate values and store it in new variable called dfc

# In[6]:


dfc = df.copy().drop_duplicates()


# In[7]:


dfc.shape


# In[8]:


dfc.info()


# #### There are missing data in the dataset. lets be more specific which columns have missing data.

# In[9]:


dfc.isnull().sum()


# #### The column "Description" and "CustomerID" have missing data

# In[10]:


dfc.nunique()


# #### The no. of unique "StockCode" and "Description" are different which need attention

# In[11]:


dfc.describe()


# #### The minimum value of Quantity is negative which is not possible,also the price of a product can't be negative.

# In[12]:


print(dfc[dfc['Quantity'] == -80995.000000])


# #### Lets see if there are any other negative value ?

# In[13]:


print(dfc[dfc['Quantity'] < 0])


# #### There are 10624 rows with negative values which can impact the analysis. Moreover the InvoiceNo. for this values starts with C.

# #### Let us check if there is any relation between Invoice no starting with "C" and Quantity with negative values ?

# In[14]:


print(dfc[dfc['Quantity'] < 0 & dfc['InvoiceNo'].astype(str).str.contains('C')])


# #### Yes this is just for negative Quantity. This can mean that C stand for all those order which were either canclled or returned.

# #### Any product listed for negative price

# In[15]:


print(dfc[dfc['UnitPrice'] < 0])


# #### There are 2 products that have a negative price, also there invoice no. start with "A"

# #### Lets see if there are any other product whose inVoice no. contains A

# In[16]:


print(dfc[dfc['InvoiceNo'].astype(str).str.contains('A')])


# #### There are total 3 Invoice ID which contains "A"

# #### As the price of the product can't be negative we will remove this rows.

# In[17]:


dfc = dfc[dfc['UnitPrice'] >= 0].copy()


# #### There are lot of missing vales in CustomerID column, we will replace them with "Unknown"

# In[18]:


dfc['CustomerID'].replace(np.nan,"Unknown", inplace=True)
dfc.CustomerID.isnull().sum()


# #### Working with null values in Description column.

# In[19]:


rows_with_null_description = df[df['Description'].isnull()]
print(rows_with_null_description)


# #### There are 1454 rows with null value. we can delete these rows.

# In[20]:


dfc = dfc.dropna(subset=['Description'])


# #### We will extract Month and Day from "InvoiceDate"

# In[21]:


dfc['InvoiceDate'] = pd.to_datetime(dfc['InvoiceDate'])


# In[22]:


dfc['Purchase_Month'] = dfc['InvoiceDate'].dt.strftime('%Y-%m')


# In[23]:


dfc['Day_of_Purchase']= dfc['InvoiceDate'].dt.day_name()


# In[24]:


print(dfc['Day_of_Purchase'].unique())


# #### The column "InvoiceDate" is of no use now so, we can delete it

# In[25]:


dfc = dfc.drop(columns=['InvoiceDate'])


# In[26]:


dfc.isnull().sum()


# #### Check for outliners

# In[27]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.boxplot(x=dfc['UnitPrice'])
plt.title('Boxplot of UnitPrice')
plt.show()


# #### There are few outliner but it's ok to have them as the price can vary product to product.

# In[28]:


plt.scatter(dfc.index, dfc['Quantity'])
plt.title('Scatter plot of Quantity')
plt.xlabel('Index')
plt.ylabel('Quantity')
plt.show()


# #### We will drop duplicates if any and save it for analysis

# In[29]:


dfc= dfc.copy().drop_duplicates()


# In[31]:


dfc.to_csv('Online_Retail_Cleaned.csv', index=False)


# ## Now let's start with the analysis

# #### We will seperate the data in 2 parts. can_order(Cancelled orders) and suc_order(successful_orders)

# #### Data of successful sales

# In[32]:


suc_data = dfc[~dfc['InvoiceNo'].str.contains('C', na=False)].copy()
suc_data


# #### Data of cancelled or returned products

# In[33]:


can_data = dfc[dfc['InvoiceNo'].str.contains('C', na=False)].copy()
can_data


# ## Sales trend

# #### Are there any seasonal patterns or trends in sales? Which  days of the week or month have the highest sales?

# In[160]:


sales_over_time= suc_data.groupby(['Purchase_Month']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
sales_over_time1 = sales_over_time.sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.lineplot(data=sales_over_time, marker='o')
plt.title('Sales Amount Per Month')
plt.xlabel('Sales Month')
plt.ylabel('Sales Amount')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# In[135]:


sales_over_week= suc_data.groupby(['Day_of_Purchase']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
sales_over_week.sort_values( ascending=False).head(5)

plt.figure(figsize=(10, 6))
sns.barplot(x=sales_over_week.index, y=sales_over_week.values)

for i, value in enumerate(sales_over_week.values):
    plt.plot(i, value, 'o', color='black', zorder=3)

plt.title('Total Sales Over Each Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Total Sales')
plt.grid(True)
plt.xticks(rotation=45)
plt.show()



# ## Product performance

# #### Which are the best-selling products?

# In[39]:


product_sales = suc_data.groupby(['StockCode', 'Description']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
product_sales.sort_values( ascending=False).head(10)


# #### Trending products each month 

# In[134]:


Trending_products = suc_data.groupby([ 'Purchase_Month', 'StockCode','Description'])['Quantity'].sum().reset_index()
Trending_products['Rank'] = Trending_products.groupby(['Purchase_Month'])['Quantity'].rank(ascending=False, method='dense')
Top_5_products_per_month = Trending_products[Trending_products['Rank'] <= 5]

Top_5_products_per_month


# ## Customer Behaviour

# #### Who are the most valuable customers in terms of total spending or frequency of purchases?

# In[41]:


customer_spending = suc_data.groupby('CustomerID')[['Quantity', 'UnitPrice']].sum()
customer_spending['total_spending'] = suc_data.groupby(['CustomerID']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
customer_spending_ranked = customer_spending.sort_values(by='total_spending', ascending=False)

customer_frequency = suc_data.groupby('CustomerID')['InvoiceNo'].nunique()
customer_frequency_ranked = customer_frequency.sort_values( ascending=False)

print("Top Customers by Total Spending:")
print(customer_spending_ranked.head(10))

print("\nTop Customers by Frequency of Purchases:")
print(customer_frequency_ranked.head(10))


# #### What is the average order size? Are there any differences in purchasing behavior between new and returning customers?

# In[42]:


average_order_size = suc_data['Quantity'].sum() / suc_data['InvoiceNo'].nunique()
print("Average Order Size:", average_order_size)

customer_purchase_counts = suc_data.groupby('CustomerID')['InvoiceNo'].nunique()
new_customers = customer_purchase_counts[customer_purchase_counts == 1].index
returning_customers = customer_purchase_counts[customer_purchase_counts > 1].index

average_order_size_new = suc_data[suc_data['CustomerID'].isin(new_customers)]['Quantity'].sum() / len(new_customers)
average_order_size_returning = suc_data[suc_data['CustomerID'].isin(returning_customers)]['Quantity'].sum() / len(returning_customers)

print("Average Order Size for New Customers:", average_order_size_new)
print("Average Order Size for Returning Customers:", average_order_size_returning)


# ## Geographic Analysis

# #### How do sales vary across different regions or countries?

# In[43]:


country_spending = suc_data.groupby('Country')[['Quantity', 'UnitPrice']].sum()
country_spending['Total_spending'] = suc_data.groupby(['Country']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())
country_spending_ranked = country_spending.sort_values(by='Total_spending', ascending=False)

country_frequency = suc_data.groupby('Country')['InvoiceNo'].nunique()
country_frequency_ranked = country_frequency.sort_values( ascending=False)

print("Top countries by Total Spending:")
print(country_spending_ranked.head(10))

print("\nTop countries by Frequency of Purchases:")
print(country_frequency_ranked.head(10))


# ## Customer Retention and Loyalty

# #### For this analysis we have considered only those customers whose CustomerID is known

# In[120]:


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
                                                                         


# ## Price analysis

# #### What is the distribution of unit prices for products?

# In[118]:


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


# ## Analyzing cancelled orders and it's impact.

# #### what's the impact of cancelled orders on overall sales?

# In[60]:


total_cancelled_amount = (can_data['UnitPrice'] * can_data['Quantity']).sum()
print("Overall loss: ",total_cancelled_amount)


# #### Comparision of successful orders and cancelled orders

# In[145]:


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


# #### Revenue lost due to cancelled orders

# In[85]:


can_over_time= can_data.groupby(['Purchase_Month']).apply(lambda x: (x['Quantity'] * x['UnitPrice']).sum())


# #### Comparision of Expected sales and actual sales

# In[146]:


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


# #### No. of Cancelled orders by day

# In[147]:


Can_per_week = can_data.groupby('Day_of_Purchase')['InvoiceNo'].nunique()
print(Can_per_week)

plt.figure(figsize=(10, 6))
sns.barplot(x=Can_per_week.index, y=Can_per_week.values)
for i, value in enumerate(Can_per_week.values):
    plt.plot(i, value, 'o', color='black')

plt.title('Cancellation Per Month')
plt.xlabel('Cancellation Month')
plt.ylabel('No. of cancellation')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# #### Which country customers have cancelled most orders

# In[133]:


Can_per_country = can_data.groupby('Country')['InvoiceNo'].nunique()
Can_per_country1 = Can_per_country.sort_values( ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=Can_per_country1.index, y=Can_per_country1.values)
plt.xlabel('Country')
plt.ylabel('Number of Cancelled Orders')
plt.title('Cancelled Orders per Country')
plt.xticks(rotation=90)
plt.show()


# #### Correlation

# In[168]:


numeric_df = suc_data.select_dtypes(include='number')
numeric_df['Total_price'] = numeric_df['Quantity'] * numeric_df['UnitPrice']
correlation_matrix = numeric_df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()


# In[167]:


numeric_df


# # Conclusion

# #### • November records the highest sales, and Thursdays emerge as the peak sales day, with an unexpected absence of sales on      Saturdays.
# #### •	The top products, ranked by total sales amount, include DOTCOM POSTAGE, REGENCY CAKESTAND 3 TIER, PAPER CRAFT, LITTLE BIRDIE, WHITE HANGING HEART T-LIGHT HOLDER, and PARTY BUNTING.
# #### •	Customer IDs 14646, 18102, 17450, 16446 and 14911 are recognized as the top customers, determined by their purchase amounts.
# #### •	The average order size among new customers is 278.52, whereas for existing customers, it stands at 1769.34.
# #### •	In terms of country-wise purchases, the United Kingdom leads with the highest purchase, followed by the Netherlands, Eire, Germany, and France.
# #### •	In terms of retention rate, November exhibits the highest rate at 38.37%, whereas January has the lowest rate at 17.07%.
# #### •	The company incurred a loss of 893,979.73 as a result of cancelled or returned products.
# #### •	November saw the highest number of orders being cancelled or returned, while December had the lowest.
# #### •	The majority of cancelled or returned orders originated from the United Kingdom.
# #### •	The correlation coefficient indicates that there is a relationship between the quantity of products ordered and the total price.

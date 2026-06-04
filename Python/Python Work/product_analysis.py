import pandas as pd


orders = pd.read_csv(r"C:\Users\Dell\Desktop\Product Performance & Customer Analytics\Dataset\olist_orders_dataset.csv")

items = pd.read_csv(r"C:\Users\Dell\Desktop\Product Performance & Customer Analytics\Dataset\olist_order_items_dataset.csv")

products = pd.read_csv(r"C:\Users\Dell\Desktop\Product Performance & Customer Analytics\Dataset\olist_products_dataset.csv")

reviews = pd.read_csv(r"C:\Users\Dell\Desktop\Product Performance & Customer Analytics\Dataset\olist_order_reviews_dataset.csv")

payments = pd.read_csv(r"C:\Users\Dell\Desktop\Product Performance & Customer Analytics\Dataset\olist_order_payments_dataset.csv")

customers = pd.read_csv(r"C:\Users\Dell\Desktop\Product Performance & Customer Analytics\Dataset\olist_customers_dataset.csv")

translation = pd.read_csv(r"C:\Users\Dell\Desktop\Product Performance & Customer Analytics\Dataset\product_category_name_translation.csv")


# Merge product and item tables
merged = items.merge(products, on="product_id")

# Merge category translation
merged = merged.merge(
    translation,
    on="product_category_name",
    how="left"
)

# Top categories by revenue
category_sales = merged.groupby(
    "product_category_name_english"
)["price"].sum().sort_values(ascending=False)

print("\nTOP 10 PRODUCT CATEGORIES BY REVENUE:\n")
print(category_sales.head(10))


# Number Of Product Sold By Category

category_quantity = merged.groupby(
    "product_category_name_english"
)["order_item_id"].count().sort_values(ascending=False)

print("\nTOP 10 PRODUCT CATEGORIES BY QUANTITY SOLD:\n")
print(category_quantity.head(10))

# Average price by category

avg_price = merged.groupby(
    "product_category_name_english"
)["price"].mean().sort_values(ascending=False)

print("\nTOP 10 CATEGORIES BY AVERAGE PRODUCT PRICE:\n")
print(avg_price.head(10))



# Merge reviews with orders
review_merge = reviews.merge(
    orders,
    on="order_id"
)

# Merge with items
review_merge = review_merge.merge(
    items,
    on="order_id"
)

# Merge with products
review_merge = review_merge.merge(
    products,
    on="product_id"
)

# Merge category translation
review_merge = review_merge.merge(
    translation,
    on="product_category_name",
    how="left"
)

# Average review score by category
avg_reviews = review_merge.groupby(
    "product_category_name_english"
)["review_score"].mean().sort_values()

print("\nLOWEST RATED PRODUCT CATEGORIES:\n")
print(avg_reviews.head(10))


# Revenue by category

revenue = review_merge.groupby(
    "product_category_name_english"
)["price"].sum()

# Average review score
ratings = review_merge.groupby(
    "product_category_name_english"
)["review_score"].mean()

# Combine both
combined = pd.concat(
    [revenue, ratings],
    axis=1
)

combined.columns = [
    "total_revenue",
    "avg_review_score"
]

# High revenue but low ratings
problem_categories = combined.sort_values(
    by=["avg_review_score", "total_revenue"],
    ascending=[True, False]
)

print("\nHIGH REVENUE BUT LOW RATED CATEGORIES:\n")
print(problem_categories.head(10))


# Convert dates
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"]
)

# Delivery days
orders["delivery_days"] = (
    orders["order_delivered_customer_date"] -
    orders["order_purchase_timestamp"]
).dt.days

# Merge orders with items
delivery_merge = orders.merge(
    items,
    on="order_id"
)

# Merge with products
delivery_merge = delivery_merge.merge(
    products,
    on="product_id"
)

# Merge category translation
delivery_merge = delivery_merge.merge(
    translation,
    on="product_category_name",
    how="left"
)

# Average delivery days by category
delivery_analysis = delivery_merge.groupby(
    "product_category_name_english"
)["delivery_days"].mean().sort_values(ascending=False)

print("\nSLOWEST DELIVERY CATEGORIES:\n")
print(delivery_analysis.head(10))


# Merge reviews into delivery data

delivery_merge = delivery_merge.merge(
    reviews,
    on="order_id",
    how="left"
)
# Revenue by category
revenue = delivery_merge.groupby(
    "product_category_name_english"
)["price"].sum()

# Average review score
ratings = delivery_merge.groupby(
    "product_category_name_english"
)["review_score"].mean()

# Average delivery days
delivery = delivery_merge.groupby(
    "product_category_name_english"
)["delivery_days"].mean()

# Combine all metrics
performance = pd.concat(
    [revenue, ratings, delivery],
    axis=1
)

performance.columns = [
    "total_revenue",
    "avg_review_score",
    "avg_delivery_days"
]

# Filter strong categories
best_categories = performance[
    (performance["total_revenue"] > 300000) &
    (performance["avg_review_score"] >= 4) &
    (performance["avg_delivery_days"] <= 12)
]

# Sort by revenue
best_categories = best_categories.sort_values(
    by="total_revenue",
    ascending=False
)

print("\nPROFITABLE AND EFFICIENT CATEGORIES:\n")
print(best_categories)



# Merge customer data

customer_merge = orders.merge(
    customers,
    on="customer_id"
)

customer_merge = customer_merge.merge(
    items,
    on="order_id"
)

customer_merge = customer_merge.merge(
    products,
    on="product_id"
)

customer_merge = customer_merge.merge(
    translation,
    on="product_category_name",
    how="left"
)

# Count purchases per customer per category

repeat_data = customer_merge.groupby(
    [
        "customer_unique_id",
        "product_category_name_english"
    ]
)["order_id"].count().reset_index()

# Keep repeated purchases only

repeat_data = repeat_data[
    repeat_data["order_id"] > 1
]

# Count repeat customers by category

repeat_categories = repeat_data.groupby(
    "product_category_name_english"
)["customer_unique_id"].count().sort_values(
    ascending=False
)

print("\nTOP CATEGORIES WITH REPEAT CUSTOMERS:\n")
print(repeat_categories.head(10))



# Visual Analysis in Python

# previous analysis code...

print(repeat_categories.head(10))


# Python visualization

import matplotlib.pyplot as plt

top_repeat = repeat_categories.head(10)

plt.figure(figsize=(10,4))

top_repeat.plot(kind="bar")

plt.title("Top Categories With Repeat Customers")

plt.xlabel("Product Category")

plt.ylabel("Repeat Customers")

plt.xticks(rotation=45)

plt.show()


# Revenue vs Ratings Scatter Plot

import seaborn as sns 
plt.figure(figsize=(10,6))

sns.scatterplot(
    data=performance,
    x="avg_review_score",
    y="total_revenue"
)

plt.title("Revenue vs Customer Ratings")

plt.xlabel("Average Review Score")

plt.ylabel("Total Revenue")

plt.show()
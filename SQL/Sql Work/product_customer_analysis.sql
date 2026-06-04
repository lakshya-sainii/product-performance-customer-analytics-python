CREATE DATABASE Product_analysis
USE Product_analysis


-- TOP PRODUCT CATEGORIES BY REVENUE


SELECT TOP 10
    t.Column2 AS product_category_name_english,
    ROUND(SUM(oi.price), 2) AS total_revenue

FROM olist_order_items_dataset oi

JOIN olist_products_dataset p
    ON oi.product_id = p.product_id

JOIN product_category_name_translation t
    ON p.product_category_name = t.Column1

GROUP BY 
    t.Column2

ORDER BY 
    total_revenue DESC;



-- 2. LOWEST RATED PRODUCT CATEGORIES


SELECT TOP 10
    t.Column2 AS product_category_name_english,
    ROUND(AVG(CAST(r.review_score AS FLOAT)), 2) AS avg_review_score,
    COUNT(r.review_id) AS total_reviews
FROM olist_order_items_dataset oi

JOIN olist_products_dataset p
    ON oi.product_id = p.product_id

JOIN product_category_name_translation t
    ON p.product_category_name = t.Column1

JOIN olist_order_reviews_dataset r
    ON oi.order_id = r.order_id

GROUP BY 
    t.Column2

ORDER BY 
    avg_review_score ASC;


 
-- 3. DELIVERY DELAY ANALYSIS BY CATEGORY


SELECT TOP 10
    t.Column2 AS product_category_name_english,

    ROUND(
        AVG(
            DATEDIFF(
                DAY,
                o.order_purchase_timestamp,
                o.order_delivered_customer_date
            ) * 1.0
        ),
        2
    ) AS avg_delivery_days,

    COUNT(o.order_id) AS total_orders

FROM olist_order_items_dataset oi

JOIN olist_products_dataset p
    ON oi.product_id = p.product_id

JOIN product_category_name_translation t
    ON p.product_category_name = t.Column1

JOIN olist_orders_dataset o
    ON oi.order_id = o.order_id

WHERE o.order_delivered_customer_date IS NOT NULL

GROUP BY 
    t.Column2

ORDER BY 
    avg_delivery_days DESC;


   
-- 4. TOP CATEGORIES WITH REPEAT CUSTOMERS

SELECT TOP 10
    t.Column2 AS product_category_name_english,

    COUNT(DISTINCT c.customer_unique_id) 
    AS repeat_customers

FROM olist_customers_dataset c

JOIN olist_orders_dataset o
    ON c.customer_id = o.customer_id

JOIN olist_order_items_dataset oi
    ON o.order_id = oi.order_id

JOIN olist_products_dataset p
    ON oi.product_id = p.product_id

JOIN product_category_name_translation t
    ON p.product_category_name = t.Column1

WHERE c.customer_unique_id IN (

    SELECT customer_unique_id
    FROM olist_customers_dataset c2

    JOIN olist_orders_dataset o2
        ON c2.customer_id = o2.customer_id

    GROUP BY customer_unique_id

    HAVING COUNT(o2.order_id) > 1
)

GROUP BY 
    t.Column2

ORDER BY 
    repeat_customers DESC;



-- 5. PROFITABLE + EFFICIENT PRODUCT CATEGORIES


SELECT TOP 10
    t.Column2 AS product_category_name_english,

    ROUND(SUM(oi.price), 2) AS total_revenue,

    ROUND(
        AVG(CAST(r.review_score AS FLOAT)),
        2
    ) AS avg_review_score,

    ROUND(
        AVG(
            DATEDIFF(
                DAY,
                o.order_purchase_timestamp,
                o.order_delivered_customer_date
            ) * 1.0
        ),
        2
    ) AS avg_delivery_days

FROM olist_order_items_dataset oi

JOIN olist_products_dataset p
    ON oi.product_id = p.product_id

JOIN product_category_name_translation t
    ON p.product_category_name = t.Column1

JOIN olist_orders_dataset o
    ON oi.order_id = o.order_id

JOIN olist_order_reviews_dataset r
    ON oi.order_id = r.order_id

WHERE o.order_delivered_customer_date IS NOT NULL

GROUP BY 
    t.Column2

HAVING 
    SUM(oi.price) > 300000
    AND AVG(CAST(r.review_score AS FLOAT)) > 4

ORDER BY 
    total_revenue DESC;
Perguntas de negócios:

--Q1. Qual é o total de receita gerada por clientes do sexo masculino Vs. feminino?
select gender, SUM(purchase_amount) as revenue
from customer
group by gender

--Q2. Quais clientes usaram um desconto, mas ainda assim gastaram mais do que o valor médio de compra?
select customer_id, purchase_amount
from customer
where discount_applied = 'Yes' and purchase_amount >= (select AVG(purchase_amount) from customer)

-- Q3. Quais são os 5 produtos com a maior classificação média de avaliações?
select item_purchased, ROUND(AVG(review_rating::numeric), 2) as "Average Product Rating"
from customer
group by item_purchased
order by avg(review_rating) desc
limit 5;

--Q4. Comparar o valor médio de compra entre o envio padrão e o envio expresso.
select shipping_type,
ROUND(AVG(purchase_amount), 2)
from customer
where shipping_type in ('Standard', 'Express')
group by shipping_type

--Q5. Os clientes assinantes gastam mais? Comparar o gasto médio e a receita total 
-- entre assinantes e não assinantes.

select subscription_status,
COUNT(customer_id) as total_customers,
ROUND(AVG(purchase_amount), 2) as avg_spend,
ROUND(SUM(purchase_amount), 2) as total_revenue
from customer
group by subscription_status
order by total_revenue, avg_spend desc;

--Q6. Quais os 5 produtos tem a maior porcentagem de compras com descontos aplicados?

select item_purchased,
ROUND(100 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END)/COUNT(*), 2) as discount_rate
from customer
group by item_purchased
order by discount_rate desc
limit 5;

--Q7. Segmentar os clientes em novos, recorrentes e fiéis com base no
-- número total de compras anteriores e mostrar a contagem de cada segmento. 

with customer_type as(
select customer_id, previous_purchases,
CASE 
	WHEN previous_purchases = 1 THEN 'New'
	WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
	ELSE 'Loyal'
	END as customer_segment
from customer
)

select customer_segment, COUNT(*) as "Number of customers"
from customer_type
group by customer_segment

--Q8. Quais são os 3 produtos mais comprados em cada categoria? 

with item_counts as (
select category,
item_purchased,
COUNT(customer_id) as total_orders,
ROW_NUMBER() over(partition by category order by count(customer_id) DESC) as item_rank
from customer
group by category, item_purchased
)

select item_rank, category, item_purchased, total_orders
from item_counts
Where item_rank <= 3;

--Q9. Serão os clientes que são compradores recorrentes também propensos a assinar?
-- Clientes recorrentes tem mais de 5 compras anteriores.

select subscription_status,
count(customer_id) as repeat_buyers
from customer
where previous_purchases > 5
group by subscription_status

--Q10. Qual a receita por faixa etária? 

select age_group,
SUM(purchase_amount) as total_revenue
from customer
group by age_group
order by total_revenue desc;
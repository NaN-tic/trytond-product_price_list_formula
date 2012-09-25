Product Price List Formula Module
#################################

The product_price_list_formula module add new features product_price_list module.

1- Add new values to compute formula:

 * product
 * party
 * quantity
 * price_list

2 - New method to compute price list from other price lista

Formula examples
################

Add 10% cost price:

 product.cost_price*1.10

Add 10% cost price and round 2 decimals:

 Decimal(round(product.cost_price*1.10,2))

Price list from other price list (from price list ID 3) and add 10%:

 price_list.compute_price_list(3)*1.10


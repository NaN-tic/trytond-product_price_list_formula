#:after:product_price_list/price_list:section:lineas_en_las_tarifas#

.. inheritref:: product_price_list_formula/price_list:section:formula

===============================
Tarifas de producto por formula
===============================

Amplia los cálculos de las reglas de tarifa por tercero.

En la fórmula podemos usar los siguientes campos:

* product
* price_list

Ejemplo de cálculos:

* Añadir un 10% al precio de coste:

  ``getattr(product, 'cost_price')*1.10``

* Añadir un 10% al precio de coste y redondeo a 2 decimales:

  ``Decimal(round(getattr(product, 'cost_price')*1.10,2))``

* Una tarifa que dependa de otra tarifa (ID 3) y le añadimos un 10%:

  ``price_list(3)*1.10``

  Este ejemplo se basa la tarifa con identificador 3. En el caso de que no
  exista esta tarifa, un mensaje de aviso le informará que la tarifa no se
  encuentra por lo que deberá usar un identificador válido.

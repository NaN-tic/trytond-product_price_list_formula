===========================
Fórmula tarifas de producto
===========================

Amplia los cálculos de las reglas de tarifa por tercero.

En la fórmula podemos usar los siguientes campos:

* product
* party
* quantity
* price_list

Ejemplo de cálculos:

* Añadir un 10% al precio de coste:

  ``product.cost_price*1.10``

* Añadir un 10% al precio de coste y redondeo a 2 decimales:

  ``Decimal(round(product.cost_price*1.10,2))``

* Una tarifa que dependa de otra tarifa y le añadimos un 10%:

  ``price_list.compute_price_list(3)*1.10``

  Este ejemplo se basa la tarifa con identificador 3. En el caso de que no
  exista esta tarifa, un mensaje de aviso le informará que la tarifa no se
  encuentra por lo que deberá usar un identificador válido.

Módulos de los que depende
==========================

Instalados
----------

.. toctree::
   :maxdepth: 1

   /company/index
   /party/index
   /product/index
   /product_price_list/index

Dependencias
------------

* Compañía_
* Producto_
* Tarifas_
* Terceros_

.. _Compañía: ../company/index.html
.. _Producto: ../product/index.html
.. _Tarifas: ../product_price_list/index.html
.. _Terceros: ../party/index.html

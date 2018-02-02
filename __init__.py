# This file is part product_price_list_formula module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import price_list


def register():
    Pool.register(
        price_list.PriceList,
        module='product_price_list_formula', type_='model')

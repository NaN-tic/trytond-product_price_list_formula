# This file is part product_price_list_formula module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.product_price_list_formula.tests.test_product_price_list_formula import suite
except ImportError:
    from .test_product_price_list_formula import suite

__all__ = ['suite']

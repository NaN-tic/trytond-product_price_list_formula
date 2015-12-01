# This file is part of the product_price_list_formula module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductPriceListFormulaTestCase(ModuleTestCase):
    'Test Product Price List Formula module'
    module = 'product_price_list_formula'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPriceListFormulaTestCase))
    return suite
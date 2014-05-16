#!/usr/bin/env python
#This file is part product_price_list_formula module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.

import sys
import os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import unittest
from decimal import Decimal

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_depends
from trytond.transaction import Transaction


class ProductPriceListFormulaTestCase(unittest.TestCase):
    '''
    Test Product Price List Formula module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('sale_price_list')
        trytond.tests.test_tryton.install_module('product_price_list_formula')
        self.price_list = POOL.get('product.price_list')
        self.company = POOL.get('company.company')
        self.uom = POOL.get('product.uom')
        self.category = POOL.get('product.category')
        self.template = POOL.get('product.template')
        self.product = POOL.get('product.product')
        self.user = POOL.get('res.user')

    def test0006depends(self):
        '''
        Test depends.
        '''
        test_depends()

    def test0010price_list(self):
        '''
        Create Price List
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            company, = self.company.search([('rec_name', '=', 'B2CK')])
            self.user.write([self.user(USER)], {
                    'main_company': company.id,
                    'company': company.id,
                    })
            CONTEXT.update(self.user.get_preferences(context_only=True))

            uom, = self.uom.search([
                    ('name', '=', 'Unit'),
                    ])
            category, = self.category.create([{
                    'name': 'Category',
                    }])
            template, = self.template.create([{
                    'name': 'Carrier',
                    'default_uom': uom.id,
                    'category': category.id,
                    'type': 'service',
                    'list_price': Decimal(0),
                    'cost_price': Decimal(0),
                    }])
            product, = self.product.create([{
                    'template': template.id,
                    }])

            price_list1, = self.price_list.create([{
                'name': 'General Price List',
                'company': company.id,
                'lines': [
                            ('create', [{
                                'formula': 'product.cost_price * 1.10',
                            }],
                        )],
                }])

            self.assert_(price_list1)


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite:
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPriceListFormulaTestCase))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

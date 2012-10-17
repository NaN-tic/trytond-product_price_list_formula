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
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
    test_depends
from trytond.transaction import Transaction
from decimal import Decimal

class ProductPriceListFormulaTestCase(unittest.TestCase):
    '''
    Test Helloword module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('sale_price_list')
        trytond.tests.test_tryton.install_module('product_price_list_formula')
        self.company = POOL.get('company.company')
        self.currency = POOL.get('currency.currency')
        self.category = POOL.get('product.category')
        self.uom = POOL.get('product.uom')
        self.product = POOL.get('product.product')
        self.price_list = POOL.get('product.price_list')
        self.price_list_line = POOL.get('product.price_list.line')

    def test0006depends(self):
        '''
        Test depends.
        '''
        test_depends()

    def test0010company(self):
        '''
        Create currency and company.
        '''
        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            currency1 = self.currency.create({
                'name': 'Currency',
                'symbol': 'C',
                'code': 'CUR'
                })
            self.assert_(currency1)

            company1 = self.company.create({
                'name': 'Zikzakmedia',
                'currency': currency1,
                })
            self.assert_(company1)

            transaction.cursor.commit()

    def test0020product(self):
        '''
        Create Product
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT) as transaction:
            Category = POOL.get('product.category')
            category = Category.create({'name': 'Toys'})
            self.assert_(category)

            uom, = self.uom.search([
                    ('name', '=', 'Unit'),
                    ])
            product = self.product.create({
                    'name': 'Carrier',
                    'default_uom': uom.id,
                    'category': category.id,
                    'type': 'service',
                    'list_price': Decimal(0),
                    'cost_price': Decimal(0),
                    })
            self.assert_(product)
            transaction.cursor.commit()

    def test0030price_list(self):
        '''
        Create Price List
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT) as transaction:
            company1 = self.currency.search([], 0, 1, None)[0]
            with transaction.set_user(0):
                price_list1 = self.price_list.create({
                    'name': 'General Price List',
                    'company': company1.id,
                    'lines': [
                        ('create', {
                            'formula': 'product.cost_price*1.10',
                            },
                        ),],
                    })

                self.assert_(price_list1)

            transaction.cursor.commit()
 
def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPriceListFormulaTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

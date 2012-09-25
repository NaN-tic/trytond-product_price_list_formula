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
            currency1_id = self.currency.create({
                'name': 'Currency',
                'symbol': 'C',
                'code': 'CUR'
                })
            self.assert_(currency1_id)

            company1_id = self.company.create({
                'name': 'Zikzakmedia',
                'currency': currency1_id,
                })
            self.assert_(company1_id)

            transaction.cursor.commit()

    def test0020product(self):
        '''
        Create Product
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT) as transaction:
            cat_obj = POOL.get('product.category')
            cat_id = cat_obj.create({'name': 'Toys'})
            self.assert_(cat_id)

            uom_obj = POOL.get('product.uom')
            values = {
                'name': 'unit',
                'symbol': 'u',
                'category': cat_id,
                'rate': 1,
                'factor': 1,
                'rounding': 2,
                'digits': 2,
            }
            uom_id = uom_obj.create(values)
            self.assert_(uom_id)

            prod_obj = POOL.get('product.product')
            values = {
                'name': 'Ball',
                'list_price': '45.32',
                'cost_price': '35.32',
                'type': 'goods',
                'default_uom': uom_id,
                'cost_price_method': 'fixed',
                'code':'BALL',
                'salable': True,
            }
            prod_id = prod_obj.create(values)
            self.assert_(prod_id)
            transaction.cursor.commit()

    def test0030price_list(self):
        '''
        Create Price List
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT) as transaction:
            company1_id = self.currency.search([], 0, 1, None)[0]
            with transaction.set_user(0):
                price_list1_id = self.price_list.create({
                    'name': 'General Price List',
                    'company': company1_id,
                    'lines': [
                        ('create', {
                            'formula': 'product.cost_price*1.10',
                            },
                        ),],
                    })

                self.assert_(price_list1_id)

            transaction.cursor.commit()
 
def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPriceListFormulaTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

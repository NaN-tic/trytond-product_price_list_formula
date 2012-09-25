#This file is part product_price_list_formula module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.tools import safe_eval, datetime_strftime
from trytond.transaction import Transaction
from trytond.pool import Pool

from decimal import Decimal

class PriceList(ModelSQL, ModelView):
    _name = 'product.price_list'

    def __init__(self):
        super(PriceList, self).__init__()
        self._error_messages.update({
            'not_found_price_list': 'Not found price list: %s!',
        })

    def _get_context_price_list_line(self, party, product, unit_price,
            quantity, uom):
        '''
        Add party and product available in formula

        :param party: the BrowseRecord of the party.party
        :param product: the BrowseRecord of the product.product
        :param unit_price: a Decimal for the default unit price in the
            company's currency and default uom of the product
        :param quantity: the quantity of product
        :param uom: the BrowseRecord of the product.uom
        :return: a dictionary
        '''
        res = super(PriceList, self)._get_context_price_list_line(
            party, product, unit_price, quantity, uom)
        res['product'] = product
        res['party'] = party
        res['quantity'] = quantity
        res['price_list'] = Pool().get('product.price_list')
        return res

    def compute_price_list(self, price_list):
        '''
        Compute price based another price list

        :param price_list: the price list id or the BrowseRecord of the
            product.price_list
        :return: the computed unit price
        '''
        if isinstance(price_list, (int, long)):
            price_list = self.browse(price_list)

        try:
            price_list.name
        except:
            self.raise_user_error('not_found_price_list', price_list)

        quantity=0
        product = Transaction().context['product']

        res = self.compute(
                        price_list,
                        Transaction().context['customer'],
                        product, 
                        Transaction().context['unit_price'],
                        quantity,
                        Transaction().context.get('uom', product.default_uom))
        return res

PriceList()

class PriceListLine(ModelSQL, ModelView):
    'Price List Line'
    _name = 'product.price_list.line'

    def check_formula(self, ids):
        '''
        Check formula
        Add new params test in context: product, customer and price list object
        '''
        price_list_obj = Pool().get('product.price_list')
        context = price_list_obj._get_context_price_list_line(None, None,
                Decimal('0.0'), 0, None)

        product = Pool().get('product.product').search([
            ('salable', '=', True),
            ], 0, 1, None)[0]
        context['product'] =  Pool().get('product.product').browse(product)
        customer = Pool().get('party.party').search([], 0, 1, None)[0]
        context['customer'] = Pool().get('party.party').browse(customer)
        context['price_list'] = Pool().get('product.price_list')

        lines = self.browse(ids)
        with Transaction().set_context(**context):
            for line in lines:
                try:
                    if not isinstance(self.get_unit_price(line), Decimal):
                        return False
                except Exception:
                    return False
        return True

PriceListLine()

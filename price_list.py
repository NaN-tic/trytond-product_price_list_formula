#This file is part product_price_list_formula module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta

from decimal import Decimal

__all__ = ['PriceList', 'PriceListLine']
__metaclass__ = PoolMeta

class PriceList:
    __name__ = 'product.price_list'

    @classmethod
    def __setup__(cls):
        super(PriceList, cls).__setup__()
        cls._error_messages.update({
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

    @classmethod
    def compute_price_list(self, price_list):
        '''
        Compute price based another price list

        :param price_list: the price list id or the BrowseRecord of the
            product.price_list
        :return: the computed unit price
        '''
        if isinstance(price_list, (int, long)):
            price_list = self(price_list)

        try:
            price_list.name
        except:
            self.raise_user_error('not_found_price_list', price_list)

        quantity=0
        product = Transaction().context['product']
        return self.compute(
                        price_list,
                        Transaction().context['customer'],
                        product, 
                        Transaction().context['unit_price'],
                        quantity,
                        Transaction().context.get('uom', product.default_uom))


class PriceListLine:
    'Price List Line'
    __name__ = 'product.price_list.line'

    @classmethod
    def __setup__(cls):
        super(PriceListLine, cls).__setup__()
        cls._error_messages.update({
                'add_product': ('Add a product before to create a price list'),
                })

    def check_formula(self):
        '''
        Check formula
        Add new params test in context: product, customer and price list object
        '''
        pool = Pool()
        PriceList = pool.get('product.price_list')
        context = PriceList()._get_context_price_list_line(None, None,
                Decimal('0.0'), 0, None)

        products = pool.get('product.product').search([], limit=1)
        if not products:
            self.raise_user_error('add_product')
        product = products[0]
        context['product'] =  pool.get('product.product')(product)
        customer = pool.get('party.party').search([], limit=1)[0]
        context['customer'] = pool.get('party.party')(customer)
        context['price_list'] = pool.get('product.price_list')

        with Transaction().set_context(**context):
            try:
                if not isinstance(self.get_unit_price(), Decimal):
                    return False
            except Exception:
                return False
        return True

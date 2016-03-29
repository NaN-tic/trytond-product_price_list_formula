#This file is part product_price_list_formula module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from decimal import Decimal
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta

__all__ = ['PriceList']


class PriceList:
    __metaclass__ = PoolMeta
    __name__ = 'product.price_list'

    @classmethod
    def __setup__(cls):
        super(PriceList, cls).__setup__()
        cls._error_messages.update({
            'not_found_price_list': 'Not found price list: %s!',
        })

    def get_context_formula(self, party, product, unit_price, quantity, uom):
        pool = Pool()
        Company = pool.get('company.company')
        Product = pool.get('product.product')

        res = super(PriceList, self).get_context_formula(
            party, product, unit_price, quantity, uom)

        if not party:
            company_id = Transaction().context.get('company')
            party = Company(company_id)
        if not product:
            # maxim recursion Product(), search first product when is None
            product, = Product.search([], limit=1)
            product.special_price = Decimal(0) # product special price
            product.list_price_supplier = Decimal(0) # product supplier price

        res['names']['party'] = party
        res['names']['product'] = product
        res['names']['quantity'] = quantity
        res['names']['uom'] = uom
        if not 'functions' in res:
            res['functions'] = {}
        res['functions']['getattr'] = getattr
        res['functions']['setattr'] = setattr
        res['functions']['hasattr'] = hasattr
        res['functions']['Decimal'] = Decimal
        res['functions']['round'] = round
        res['functions']['compute_price_list'] = self.compute_price_list

        return res

    @classmethod
    def compute_price_list(self, pricelist):
        '''
        Compute price based another price list
        '''

        price_list = None
        if isinstance(pricelist, (int, long)):
            try:
                price_list = self(pricelist)
            except:
                pass

        if not price_list:
            self.raise_user_error('not_found_price_list', pricelist)

        context = Transaction().context
        return price_list.compute(
                    context.get('party'),
                    context.get('product'),
                    context.get('unit_price'),
                    context.get('quantity', 0),
                    context.get('uom'))

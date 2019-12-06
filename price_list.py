# This file is part product_price_list_formula module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['PriceList']

def _getattr(obj, name):
    'Proxy method because simpleeval warns against using getattr'
    return getattr(obj, name)

def _setattr(obj, name, value):
    'Proxy method because simpleeval warns against using setattr'
    return setattr(obj, name, value)


class PriceList(metaclass=PoolMeta):
    __name__ = 'product.price_list'

    def get_context_formula(self, party, product, unit_price, quantity, uom,
            pattern=None):
        pool = Pool()
        Company = pool.get('company.company')
        Product = pool.get('product.product')

        # set params context formula in Transaction context
        # in case use compute_price_list
        Transaction().context['pricelist'] = {
            'party': party,
            'product': product,
            'unit_price': unit_price,
            'quantity': quantity,
            'uom': uom,
            }
        res = super(PriceList, self).get_context_formula(
            party, product, unit_price, quantity, uom, pattern=pattern)

        if not party:
            company_id = Transaction().context.get('company')
            party = Company(company_id)
        if not product:
            # maxim recursion Product(), search first product when is None
            product, = Product.search([], limit=1)
            if hasattr(product, 'special_price'):
                product.special_price = Decimal(0)  # product special price

        res['names']['party'] = party
        res['names']['product'] = product
        res['names']['quantity'] = quantity
        res['names']['uom'] = uom
        if 'functions' not in res:
            res['functions'] = {}
        res['functions']['getattr'] = _getattr
        res['functions']['setattr'] = _setattr
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
        if isinstance(pricelist, int):
            try:
                price_list = self(pricelist)
            except:
                pass

        if not price_list:
            raise UserError(gettext(
                'product_price_list_formula.not_found_price_list',
                    priceList=pricelist))

        context = Transaction().context['pricelist']
        return price_list.compute(
                    context['party'],
                    context['product'],
                    context['unit_price'],
                    context['quantity'],
                    context['uom'],
                    )

    def compute(self, party, product, unit_price, quantity, uom, pattern=None):
        if pattern is None:
            pattern = {}
        if product and product.categories:
            pattern['category'] = (product.categories[0].id)
        return super(PriceList, self).compute(party, product, unit_price,
            quantity, uom, pattern)

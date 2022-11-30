# This file is part product_price_list_formula module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError

def _getattr(obj, name):
    'Proxy method because simpleeval warns against using getattr'
    return getattr(obj, name)

def _setattr(obj, name, value):
    'Proxy method because simpleeval warns against using setattr'
    return setattr(obj, name, value)

def simpleeval_round(value, ndigits=None):
    'round() wrapper that accepts Decimal in ndigits parameter. '
    'decistmt() used by product_price_list converts integers to floats'
    return round(value, None if ndigits is None else int(ndigits))


class PriceList(metaclass=PoolMeta):
    __name__ = 'product.price_list'

    def get_context_formula(self, party, product, unit_price, quantity, uom,
            pattern=None):
        pool = Pool()
        Company = pool.get('company.company')
        Product = pool.get('product.product')

        # set params context formula in Transaction context
        # in case use compute_price_list
        price_list_context = {
            'party': party,
            'product': product,
            'unit_price': unit_price,
            'quantity': quantity,
            'uom': uom,
            }
        Transaction().set_context(pricelist=price_list_context)
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
        res['functions']['round'] = simpleeval_round
        res['functions']['compute_price_list'] = self.compute_price_list

        return res

    @classmethod
    def compute_price_list(self, pricelist):
        '''
        Compute price based another price list
        '''

        price_list = None
        if not isinstance(pricelist, self.__class__):
            # Use int() because decistmt() used by product_price_list
            # converts integers to Decimal
            try:
                price_list = self(int(pricelist))
            except:
                pass

        if not price_list:
            raise UserError(gettext(
                'product_price_list_formula.not_found_price_list',
                    priceList=pricelist))

        context = Transaction().context['pricelist']
        value = price_list.compute(
                    context['party'],
                    context['product'],
                    context['unit_price'],
                    context['quantity'],
                    context['uom'],
                    )
        return value or Decimal(0)

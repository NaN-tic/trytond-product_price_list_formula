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

    def get_context_formula(self, product, quantity, uom, pattern=None):
        pool = Pool()
        Product = pool.get('product.product')

        # set params context formula in Transaction context
        # in case use compute_price_list
        price_list_context = {
            'product': product and product.id,
            'quantity': quantity,
            'uom': uom and uom.id,
            }
        Transaction().set_context(pricelist=price_list_context)
        res = super(PriceList, self).get_context_formula(
            product, quantity, uom, pattern)

        if not product:
            # maxim recursion Product(), search first product when is None
            product, = Product.search([], limit=1)
            if hasattr(product, 'special_price'):
                product.special_price = Decimal(0)  # product special price

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
        pool = Pool()
        Product = pool.get('product.product')
        Uom = pool.get('product.uom')

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

        context = Transaction().context.get('pricelist', {})
        product_id = context.get('product')
        quantity = context.get('quantity')
        uom_id = context.get('uom')

        value = price_list.compute(
                    Product(product_id) if product_id else None,
                    quantity,
                    Uom(uom_id) if uom_id else None,
                    )
        return value or Decimal(0)

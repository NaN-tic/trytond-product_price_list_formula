import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.account.tests.tools import (create_chart,
                                                 create_fiscalyear,
                                                 get_accounts)
from trytond.modules.account_invoice.tests.tools import (
    create_payment_term, set_fiscalyear_invoice_sequences)
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Install product_price_list_formula
        config = activate_modules(
            ['product_price_list_formula', 'sale_price_list'])

        # Create company
        _ = create_company()
        company = get_company()

        # Reload the context
        User = Model.get('res.user')
        Group = Model.get('res.group')
        config._context = User.get_preferences(True, config.context)

        # Create sale user
        sale_user = User()
        sale_user.name = 'Sale'
        sale_user.login = 'sale'
        sale_group, = Group.find([('name', '=', 'Sales')])
        sale_user.groups.append(sale_group)
        sale_user.save()

        # Create fiscal year
        fiscalyear = set_fiscalyear_invoice_sequences(
            create_fiscalyear(company))
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)
        accounts = get_accounts(company)
        revenue = accounts['revenue']
        expense = accounts['expense']

        # Create parties
        Party = Model.get('party.party')
        customer = Party(name='Customer')
        customer.save()

        # Create account category
        ProductCategory = Model.get('product.category')
        account_category = ProductCategory(name="Account Category")
        account_category.accounting = True
        account_category.account_expense = expense
        account_category.account_revenue = revenue
        account_category.save()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'goods'
        template.salable = True
        template.list_price = Decimal('100')
        template.cost_price_method = 'fixed'
        template.account_category = account_category
        product, = template.products
        product.cost_price = Decimal('57.3434')
        template.save()
        product, = template.products

        # Create payment term
        payment_term = create_payment_term()
        payment_term.save()

        # Create a price List and assign it to customer
        PriceList = Model.get('product.price_list')
        price_list1 = PriceList(name='10% over cost price')
        price_list_line = price_list1.lines.new()
        price_list_line.product = product
        price_list_line.formula = 'getattr(product, "cost_price") * 1.10'
        price_list1.save()
        price_list2 = PriceList(name='10% over cost price with 2 decimals')
        price_list_line = price_list2.lines.new()
        price_list_line.product = product
        price_list_line.formula = 'Decimal(round(getattr(product, "cost_price") * 1.10, 2))'
        price_list2.save()
        price_list3 = PriceList(name='10% over "10% over cost price" pricelist')
        price_list_line = price_list3.lines.new()
        price_list1_id = price_list1.id
        price_list_line.formula = 'compute_price_list(%s) * 1.10' % price_list1_id
        price_list3.save()

        # Use the price list on sale
        customer.sale_price_list = price_list1
        customer.save()
        config.user = sale_user.id
        Sale = Model.get('sale.sale')
        sale = Sale()
        sale.party = customer
        self.assertEqual(sale.price_list, price_list1)
        sale.payment_term = payment_term
        sale_line = sale.lines.new()
        sale_line.product = product
        self.assertEqual(sale_line.unit_price, Decimal('63.0777'))
        customer.sale_price_list = price_list2
        customer.save()
        config.user = sale_user.id
        Sale = Model.get('sale.sale')
        sale = Sale()
        sale.party = customer
        self.assertEqual(sale.price_list, price_list2)
        sale.payment_term = payment_term
        sale_line = sale.lines.new()
        sale_line.product = product
        self.assertEqual(sale_line.unit_price, Decimal('63.0800'))
        customer.sale_price_list = price_list3
        customer.save()
        config.user = sale_user.id
        Sale = Model.get('sale.sale')
        sale = Sale()
        sale.party = customer
        self.assertEqual(sale.price_list, price_list3)
        sale.payment_term = payment_term
        sale_line = sale.lines.new()
        sale_line.product = product
        self.assertEqual(sale_line.unit_price, Decimal('69.3855'))

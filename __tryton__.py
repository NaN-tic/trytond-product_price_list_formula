#This file is part product_price_list_formula module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
{
    'name': 'Product Price List Formula',
    'name_ca_ES': 'Formules tarifes de producte',
    'name_es_ES': 'Formulas tarifas de producto',
    'version': '2.4.0',
    'author': 'Zikzakmedia',
    'email': 'zikzak@zikzakmedia.com',
    'website': 'http://www.zikzakmedia.com/',
    'description': '''Add party and product in formula price list rules by parties.''',
    'description_ca_ES': '''Afegeix party i product a les formules per les regles de tarifa per tercer.''',
    'description_es_ES': 'Añade party y product a las fórmulas para las reglas de tarifa por tercero.',
    'depends': [
        'ir',
        'res',
        'product_price_list',
    ],
    'xml': [
    ],
    'translation': [
        'locale/ca_ES.po',
        'locale/es_ES.po',
    ]
}

# -*- coding: utf-8 -*-
# Copyright 2009 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Pricelist Discount',
    'version': '10.0.0.1.2',
    'category': 'Sales Management',
    'description': """Add discount in pricelist""",
    'author': 'SYLEAM',
    'depends': [
        'base',
        'product',
        'sale',
    ],
    'data': [
        'views/product_pricelist_item.xml',
    ],
    'installable': True,
    'active': False,
    'license': 'AGPL-3',
}

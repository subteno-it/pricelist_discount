# -*- coding: utf-8 -*-
################################################################
#
# pricelist_discount module for OpenERP, Pricelist Discount
# Copyright (C) 2009 SYLEAM Info Services (<http://www.Syleam.fr/>)
#                 {PROGRAMMER'S NAME AND E.MAIL ADDRESS GOES HERE
#                 THERE IS AS MANY LINE AS DEVELOPPERS INVOLVED}
#
# This file is a part of pricelist_discount
#
# pricelist_discount is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pricelist_discount is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
################################################################

{
    'name': 'Pricelist Discount',
    'version': '0.0.1',
    'category': 'Custom',
    'description': """Product""",
    'author': 'SYLEAM Info Services',
    'depends': [
            'base',
            'product',
        ],
    'init_xml': [],
    'update_xml': [
        'view/product_pricelist_item_view.xml',
        ],
    'demo_xml': [],
    'installable': True,
    'active': False,
    'license': 'GPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
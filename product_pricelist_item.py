# -*- coding: utf-8 -*-
################################################################
#
# pricelist_discount module for OpenERP, Pricelist Discount
# Copyright (C) 2009-20112 SYLEAM Info Services (<http://www.Syleam.fr/>)
#
# This file is a part of pricelist_discount
#
# pricelist_discount is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pricelist_discount is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################

from osv import osv
from osv import fields

class product_pricelist_item(osv.osv):
    """
    OpenERP Model : product.pricelist.item
    """
    _name = 'product.pricelist.item'
    _inherit = 'product.pricelist.item'

    _columns = {
        'discount': fields.float('Discount (%)', digits=(16, 2)),
        }

    _defaults = {
        'discount': lambda *a: 0.0,
        }

product_pricelist_item()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

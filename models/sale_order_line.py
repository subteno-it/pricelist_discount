# -*- coding: utf-8 -*-
##############################################################################
#
#    pricelist_discount module for OpenERP, Pricelist Discount
#    Copyright (C) 2009 SYLEAM Info Services (<http://www.syleam.fr/>)
#              Jean-Sébastien SUZANNE <jean-sebastien.suzanne@syleam.fr>
#    Copyright (C) 2012 SYLEAM Info Services (<http://www.syleam.fr/>)
#              Benoît MOTTIN <benoit.mottin@syleam.fr>
#              Sebastien LANGE <sebastien.lange@syleam.fr>
#    Copyright (C) 2016 SYLEAM Info Services (<http://www.syleam.fr/>)
#              Chris TRIBBECK <chris.tribbeck@syleam.fr>
#
#    This file is a part of pricelist_discount
#
#    pricelist_discount is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pricelist_discount is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def get_discount(self):
        """
        Get the discount for the appropriate item
        """
        if self.order_id.pricelist_id and self.product_id and self.order_id.partner_id:
            qtys = [(self.product_id, self.product_uom_qty, self.order_id.partner_id.id)]
            pricelist_item_id = self.order_id.pricelist_id._price_rule_get_multi(self.order_id.pricelist_id, qtys)[self.product_id.id][1]
            self.discount = self.env['product.pricelist.item'].browse(pricelist_item_id).discount
            print '######', self.discount


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

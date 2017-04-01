# -*- coding: utf-8 -*-
# Copyright 2017 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


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

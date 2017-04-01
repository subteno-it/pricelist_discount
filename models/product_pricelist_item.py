# -*- coding: utf-8 -*-
# Copyright 2017 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields
from odoo.addons import decimal_precision as dp


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    discount = fields.Float(string='Discount (%)', digits_compute=dp.get_precision('Product Price'), help='Discount on this pricelist item')

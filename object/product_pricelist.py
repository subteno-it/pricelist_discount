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

from osv import osv
from product._common import rounding
from tools.translate import _
import time

class product_pricelist(osv.osv):

    _inherit = "product.pricelist"

    def price_get(self, cr, uid, ids, prod_id, qty, partner=None, context=None):
#FIXME do we realy need to copy standard code rather than call super method ?
        '''
        context = {
            'uom': Unit of Measure (int),
            'partner': Partner ID (int),
            'date': Date of the pricelist (%Y-%m-%d),
        }
        '''
        context = context or {}
        currency_obj = self.pool.get('res.currency')
        product_obj = self.pool.get('product.product')
        supplierinfo_obj = self.pool.get('product.supplierinfo')
        price_type_obj = self.pool.get('product.price.type')

        if context and ('partner_id' in context):
            partner = context['partner_id']
        context['partner_id'] = partner
        date = time.strftime('%Y-%m-%d')
        if context and ('date' in context):
            date = context['date']
        result = {}
        for id in ids:
            cr.execute('SELECT * ' \
                    'FROM product_pricelist_version ' \
                    'WHERE pricelist_id = %s AND active=True ' \
                        'AND (date_start IS NULL OR date_start <= %s) ' \
                        'AND (date_end IS NULL OR date_end >= %s) ' \
                    'ORDER BY id LIMIT 1', (id, date, date))
            plversion = cr.dictfetchone()
            if not plversion:
                raise osv.except_osv(_('Warning !'),
                        _('No active version for the selected pricelist !\n' \
                                'Please create or activate one.'))

            cr.execute('SELECT id, categ_id ' \
                    'FROM product_template ' \
                    'WHERE id = (SELECT product_tmpl_id ' \
                        'FROM product_product ' \
                        'WHERE id = %s)', (prod_id,))
            tmpl_id, categ = cr.fetchone()
            categ_ids = []
            while categ:
                categ_ids.append(str(categ))
                cr.execute('SELECT parent_id ' \
                        'FROM product_category ' \
                        'WHERE id = %s', (categ,))
                categ = cr.fetchone()[0]
                if str(categ) in categ_ids:
                    raise osv.except_osv(_('Warning !'),
                            _('Could not resolve product category, ' \
                                    'you have defined cyclic categories ' \
                                    'of products!'))
            if categ_ids:
                categ_where = '(categ_id IN %s)'
                sqlargs = (tuple(categ_ids),)
            else:
                categ_where = '(categ_id IS NULL)'
                sqlargs = ()

            cr.execute(
                'SELECT i.*, pl.currency_id '
                'FROM product_pricelist_item AS i, '
                    'product_pricelist_version AS v, product_pricelist AS pl '
                'WHERE (product_tmpl_id IS NULL OR product_tmpl_id = %s) '
                    'AND (product_id IS NULL OR product_id = %s) '
                    'AND (' + categ_where + ' OR (categ_id IS NULL)) '
                    'AND price_version_id = %s '
                    'AND (min_quantity IS NULL OR min_quantity <= %s) '
                    'AND i.price_version_id = v.id AND v.pricelist_id = pl.id '
                'ORDER BY sequence LIMIT 1',
                (tmpl_id, prod_id) + sqlargs + (plversion['id'], qty))
            res = cr.dictfetchone()
            if res:
                if res['base'] == -1:
                    if not res['base_pricelist_id']:
                        price = 0.0
                    else:
                        price_tmp = self.price_get(cr, uid,
                                [res['base_pricelist_id']], prod_id,
                                qty)[res['base_pricelist_id']]
                        ptype_src = self.browse(cr, uid,
                                res['base_pricelist_id']).currency_id.id
                        price = currency_obj.compute(cr, uid, ptype_src,
                                res['currency_id'], price_tmp, round=False)
                elif res['base'] == -2:
                    where = []
                    if partner:
                        where = [('name', '=', partner)]
                    sinfo = supplierinfo_obj.search(cr, uid,
                            [('product_id', '=', tmpl_id)] + where)
                    price = 0.0
                    if sinfo:
                        cr.execute('SELECT * ' \
                                'FROM pricelist_partnerinfo ' \
                                'WHERE suppinfo_id IN %s ' \
                                    'AND min_quantity <= %s ' \
                                'ORDER BY min_quantity DESC LIMIT 1',
                                   (tuple(sinfo), qty))
                        res2 = cr.dictfetchone()
                        if res2:
                            price = res2['price']
                else:
                    price_type = price_type_obj.browse(cr, uid, int(res['base']))
                    price = currency_obj.compute(cr, uid,
                            price_type.currency_id.id, res['currency_id'],
                            product_obj.price_get(cr, uid, [prod_id],
                                price_type.field)[prod_id], round=False, context=context)

                price_limit = price

                price = price * (1.0 + (res['price_discount'] or 0.0))
                price = rounding(price, res['price_round'])
                price += (res['price_surcharge'] or 0.0)
                if res['price_min_margin']:
                    price = max(price, price_limit + res['price_min_margin'])
                if res['price_max_margin']:
                    price = min(price, price_limit + res['price_max_margin'])
            else:
                # False means no valid line found ! But we may not raise an
                # exception here because it breaks the search
                price = False
            result[id] = price
            result['discount'] = res.get('discount', 0)
            if context and ('uom' in context):
                product = product_obj.browse(cr, uid, prod_id)
                uom = product.uos_id or product.uom_id
                result[id] = self.pool.get('product.uom')._compute_price(cr,
                        uid, uom.id, result[id], context['uom'])
        return result

product_pricelist()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

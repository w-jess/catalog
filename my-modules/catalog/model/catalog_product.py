# -*- coding: utf-8 -*-
# @File  : catalog_product.py
# @Author: Whx
# @Date  : 2022/3/29
# @Desc  : 产品

from odoo import api, fields, models, _

class CatalogProduct(models.Model):
    _name = 'catalog.product'
    _description = '产品'
    _rec_name = 'name'

    # 产品号、产品名、生产商、品牌、规格
    pid = fields.Char(string='产品号', required=True, copy=False, readonly=True,
                        index=True, default=lambda self: _('New'))
    name = fields.Char(string='产品名', required=True)
    brand = fields.Char(string='品牌', required=True)
    spec = fields.Integer(string='规格', required=True)
    metric = fields.Selection([('g', 'g'), ('ml', 'ml')], string='计量单位', required=True)

    @api.model
    def create(self, vals):
        if vals.get('pid', _('New')) == _('New'):
            vals['pid'] = self.env['ir.sequence'].next_by_code('catalog.product') or _('New')
        res = super(CatalogProduct, self).create(vals)
        return res

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.pid + ']' + ' ' + rec.name
            result.append((rec.id, name))
        return result
# -*- coding: utf-8 -*-
# @File  : catalog_product.py
# @Author: Whx
# @Date  : 2022/3/29
# @Desc  : 产品

from odoo import api, fields, models

class CatalogProduct(models.Model):
    _name = 'catalog.product'
    _description = '产品'

    name = fields.Char(string='药品名')
    provider_name = fields.Many2one('catalog.provider', string=u'供应商')
    brand = fields.Char(string='品牌')
    provider_site = fields.Char(string='生产地址')
    barcode = fields.Char(string='条码号')
    spec = fields.Selection([('box', '盒'), ('bottle', '瓶')], string='规格')
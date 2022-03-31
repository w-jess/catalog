# -*- coding: utf-8 -*-
# @File  : catalog_sale.py
# @Author: Whx
# @Date  : 2022/3/29
# @Desc  : 订单

from odoo import api,fields,models

class CatalogSale(models.Model):
    _name = 'catalog.sale'
    _description = '订单'

    # 药品名、品牌、规格、数量、进货价、出售价、客户、地址
    # brand = fields.Many2one('catalog.deal', string=u'品牌')
    # spec = fields.Many2one('catalog.deal', string=u'规格')
    # quantity = fields.Integer(string='数量')
    # cost = fields.Many2one('catalog.deal', string=u'进货价')
    # shipping = fields.Integer(string='出售价')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    com_name = fields.Many2one('catalog.client', string='客户')
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    name = fields.Many2one('catalog.deal', string=u'药品名')
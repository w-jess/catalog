# -*- coding: utf-8 -*-
# @File  : catalog_purchase.py
# @Author: Whx
# @Date  : 2022/4/7
# @Desc  : 采购

from odoo import api, fields, models, _

class CatalogPurchase(models.Model):
    _name = 'catalog.purchase'
    _description = 'Purchase'
    _inherit = ['mail.thread']
    _order = 'o_name desc'

    # 订单号、药品名、品牌、规格、数量、进货价、出售价、客户、地址
    o_name = fields.Char(string='订单号', required=True, copy=False, readonly=True,
                         states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('o_name', _('New')) == _('New'):
            vals['o_name'] = self.env['ir.sequence'].next_by_code('catalog.purchase') or _('New')
        res = super(CatalogPurchase, self).create(vals)
        return res

    com_name_id = fields.Many2one('catalog.provider', string='供应商', required=True)
    date_order = fields.Date(string='订购日期', required=True, readonly=True, index=True, copy=False,
                             states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                             default=fields.Date.today)
    state = fields.Selection([
        ('draft', '询价单'),
        ('sent', '询价单已发送'),
        ('purchase', '采购订单'),
        ('done', 'Locked'),
        ('cancel', '取消'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    create_user_id = fields.Many2one('res.users', string='销售员', default=lambda self: self.env.user, readonly=True)
    # purchase_line_ids = fields.One2many('sale.lines', 'sale_id', string='Sale Lines', tracking=True)

    def action_confirm(self):
        self.state = 'purchase'

    def action_cancel(self):
        self.state = 'cancel'
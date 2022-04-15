# -*- coding: utf-8 -*-
# @File  : catalog_picking.py
# @Author: Whx
# @Date  : 2022/4/11
# @Desc  : 出库单
from odoo import api,fields,models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class CatalogPicking(models.Model):
    _name = 'catalog.picking'
    _description = '出入货单'
    _inherit = ['mail.thread']
    _rec_name = 'o_pick'

    o_pick = fields.Char(string='出货单', required=True, copy=False, readonly=True,
                         index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('o_pick', _('New')) == _('New'):
            vals['o_pick'] = self.env['ir.sequence'].next_by_code('catalog.picking') or _('New')
        res = super(CatalogPicking, self).create(vals)
        return res

    company_id = fields.Many2one('catalog.client', string='客户', required=True)
    date = fields.Datetime(string='安排的日期', required=True, readonly=True, index=True, copy=False,
                             default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', '草稿'),
        ('waiting', '等待其他操作'),
        ('confirmed', '正在等待'),
        ('assigned', '就绪'),
        ('done', '完成'),
        ('cancel', '取消'),
    ], string='Status', default='draft',
        copy=False, index=True, readonly=True, store=True, tracking=True)
    origin = fields.Char(
        '源文档', index=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},)
    create_user_id = fields.Many2one('res.users', string='销售员', default=lambda self: self.env.user)
    pack_line_ids = fields.One2many('pick.lines', 'pick_line_id', string='Pick Lines')
    pick_id = fields.Many2one('catalog.sale', string='CatalogSale')

class PickLines(models.Model):
    _name = 'pick.lines'

    pick_line_id = fields.Many2one('catalog.picking', string='货单号')
    pick_name = fields.Many2one('sale.lines', string='产品名', required=True)
    quantity_done = fields.Integer(string='完成')
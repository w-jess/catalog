# -*- coding: utf-8 -*-
# @File  : catalog_sale.py
# @Author: Whx
# @Date  : 2022/3/29
# @Desc  : 订单

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CatalogSale(models.Model):
    _name = 'catalog.sale'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '订单'
    _order = 'o_name desc'
    _rec_name = 'o_name'

    # 订单号、药品名、品牌、规格、数量、进货价、出售价、客户、地址
    o_name = fields.Char(string='单号', required=True, copy=False, readonly=True,
                         states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('o_name', _('New')) == _('New'):
            vals['o_name'] = self.env['ir.sequence'].next_by_code('catalog.sale') or _('New')
        res = super(CatalogSale, self).create(vals)
        return res

    com_name_id = fields.Many2one('catalog.client', string='客户', required=True,
                                  states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                  track_visibility='onchange')
    date_order = fields.Datetime(string='订购日期', required=True, readonly=True, index=True, copy=False,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                 default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', '报价单'),
        ('sent', '报价单已发送'),
        ('sale', '订单'),
        ('done', '订单已完成'),
        ('cancel', '取消'),
    ], string='状态', readonly=True, copy=False, index=True, tracking=3, default='draft', track_visibility='onchange')
    create_user_id = fields.Many2one('res.users', string='销售员', default=lambda self: self.env.user, readonly=True)
    sale_line_ids = fields.One2many('sale.lines', 'sale_id', string='Sale Lines')
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    picking_ids = fields.One2many('catalog.picking', 'pick_id', string='Catalog Picking')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_quotation_send(self):
        self.ensure_one()
        if not self.com_name_id.email:
            raise UserError('该公司%s未设置邮箱，无法发送！' % self.com_name_id.name)
        template_id = self.env.ref('catalog.catalog_sale_email_template').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    def preview_sale_order(self):
        action = self.env.ref('catalog.catalog_deal_act_window').read()[0]
        # action['domain'] = [('name_id.pro_id', '=', self.sale_line_ids.sale_name.pro_id)]
        return action

    def action_confirm(self):
        for rec in self:
            rec.state = 'sale'

    def action_catalog_picking(self):
        for order in self:
            if not order.sale_line_ids:
                return
            self.env['catalog.picking'].create([{
                'company_id': self.com_name_id.id,
                'origin': self.o_name,
                'create_user_id': self.create_user_id.id,
                'pick_id': self.id
            }])
            val = self.env['catalog.picking'].search([('pick_id', '=', self.id)])
            self.env['pick.lines'].create([{
                'pick_line_id': val.id,
                'pick_name': self.sale_line_ids.sale_name.id,
            }])

    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(order.picking_ids)

    def action_view_delivery(self):
        action = self.env.ref('catalog.catalog_picking_act_window').read()[0] # 获取全部分拣单

        pickings = self.mapped('picking_ids') # 获取记录集里与本次销售订单相关的分拣单
        if len(pickings) > 1:   # 如果获取到的分拣单数大于1，就过滤出id在当前记录集里的记录显示
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:  # 如果只有一个分拣单,就以form视图显示它
            action['views'] = [(self.env.ref('catalog.catalog_picking_form_view').id, 'form')]
            action['res_id'] = pickings.id
        return action


class SaleLines(models.Model):
    _name = 'sale.lines'
    _description = '订单明细'
    _rec_name = 'sale_name'

    sale_id = fields.Many2one('catalog.sale', string="订单号")
    sale_name = fields.Many2one('catalog.product', string='产品名', required=True)
    quantity = fields.Integer(string='数量', required=True)
    unit = fields.Float(string='单价', required=True)
    total = fields.Float(string='总价', digits=(12, 2), store=True)

    @api.model
    def create(self, vals):
        res = super(SaleLines, self).create(vals)
        return res

    @api.onchange('quantity', 'unit')
    def _onchange_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.unit

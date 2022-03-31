from odoo import api, fields, models

class CatalogDeal(models.Model):
    _name = 'catalog.deal'
    _description = '库存'
    _inherit = 'catalog.product'

    cost = fields.Integer(string='进货价')
    shipping = fields.Integer(string='建议出货价')
    quantity = fields.Integer(string='数量')
    create_user_id = fields.Many2one('res.users', string='操作人', default=lambda self: self.env.user, readonly=True)
    note = fields.Text(string='说明')
from odoo import api, fields, models, _

class CatalogDeal(models.Model):
    _name = 'catalog.deal'
    _description = '库存'
    _rec_name = 'name_id'

    # deal_id = fields.Many2one('catalog.deal', string="CatalogDeal")
    # 药品名、条码号、进货价/元、数量、说明、操作人
    name_id = fields.Many2one('catalog.product', string='药品名', required=True)
    site_id = fields.Many2one('catalog.warehourse', string='仓库', required=True)
    cost = fields.Float(string='进货价')
    quantity = fields.Integer(string='数量')
    barcode = fields.Char(string='条码号', required=True, copy=False, readonly=True,
                        index=True, default=lambda self: _('new'))
    create_user_id = fields.Many2one('res.users', string='操作人', default=lambda self: self.env.user, readonly=True)
    note = fields.Text(string='说明')
    date_start = fields.Date('Start Date', help="Start date for this vendor price", required=True)
    date_end = fields.Date('End Date', help="End date for this vendor price", required=True)

    @api.model
    def create(self, vals):
        if vals.get('o_name', _('new')) == _('new'):
            vals['barcode'] = self.env['ir.sequence'].next_by_code('catalog.deal') or _('new')
        res = super(CatalogDeal, self).create(vals)
        return res

# -*- coding: utf-8 -*-
# @File  : catalog_provider.py
# @Author: Whx
# @Date  : 2022/3/26
# @Desc  : 供应商
from odoo import api,fields,models

class CatalogProvider(models.Model):
    _name = 'catalog.provider'
    _description = 'Provider'

    name = fields.Char(string="公司名")
    partner_id = fields.Char(string="联系人")
    phone = fields.Integer(string="电话")
    email = fields.Char(string="Email")
    street = fields.Char(string='地址')
    city = fields.Char(string='城市')
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
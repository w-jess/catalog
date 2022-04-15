# -*- coding: utf-8 -*-
# @File  : catalog_provider.py
# @Author: Whx
# @Date  : 2022/3/26
# @Desc  : 供应商
from odoo import api,fields,models

class CatalogProvider(models.Model):
    _name = 'catalog.provider'
    _description = 'Provider'
    _rec_name = 'name'

    name = fields.Char(string="公司名", required=True)
    partner_id = fields.Char(string="联系人")
    phone = fields.Integer(string="电话")
    tel = fields.Integer(string="手机")
    email = fields.Char(string="Email", required=True)
    street = fields.Char(string='地址', required=True)
    city = fields.Char(string='城市')
    state_id = fields.Many2one("res.country.state", string='省份', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
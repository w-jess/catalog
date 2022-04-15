# -*- coding: utf-8 -*-
# @File  : catalog_warehourse.py
# @Author: Whx
# @Date  : 2022/4/7
# @Desc  : 仓库

from odoo import api, fields, models, _

class CatalogWarehourse(models.Model):
    _name = 'catalog.warehourse'
    _description = '仓库'
    # _rec_name字段负责显示Form的标题栏
    _rec_name = 'abbr'

    abbr = fields.Char(string='缩写', required=True)
    ware = fields.Char(string='仓库', required=True)
    site = fields.Many2one('catalog.client', string='地址', required=True)
# -*- coding: utf-8 -*-
# @File  : catalog_client.py
# @Author: Whx
# @Date  : 2022/3/29
# @Desc  : 客户
from odoo import api,fields,models

class CatalogClient(models.Model):
    _name = 'catalog.client'
    _inherit = 'catalog.provider'
    _rec_name = 'name'
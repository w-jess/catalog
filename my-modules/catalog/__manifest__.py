# -*- coding: utf-8 -*-
{
    'name': "catalog",

    'summary': """
        进销存系统""",

    'description': """
        进销存系统
        主要实现的功能包含：药品的进销存操作、客户管理、供应商管理、经营数据统计、数据导出、系统管理等模块
    """,
    'author': "whx",
    'website': "todo",

    'version': '13.0.1.0',

    'depends': ['base', 'mail'],
    'data': [
        "security/ir.model.access.csv",
        "data/data.xml",
        "data/message.xml",
        "reports/report.xml",
        "reports/pick_lines.xml",
        "views/catalog_sale_view.xml",
        "views/catalog_purchase_view.xml",
        "views/catalog_deal_view.xml",
        "views/catalog_picking_view.xml",
        "views/catalog_product_view.xml",
        "views/catalog_warehourse_view.xml",
        "views/catalog_provider_view.xml",
        "views/catalog_client_view.xml",
        "views/catalog_deal_menu.xml"
    ],
    # 'installable': True,
    'application': True,
}
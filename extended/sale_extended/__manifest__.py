{
    'name': "sale_extended",

    'summary': "Module to extended Funtionts Sale",

    'author': "danloveper",

    'category': 'Sales/Sales',
    'version': '19.0.1',

    'depends': [
        'stock',
        'sale',
        'sale_management',
        'contacts',
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/ir.sequence.xml',
        'data/integration_cron.xml',
        'views/integration_sale_order_views.xml',
    ],
}


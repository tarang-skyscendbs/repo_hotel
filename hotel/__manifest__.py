{
    'name': 'hotel management',
    'description': 'This module will be use to manage hotel features',
    'summary': 'for room management',
    'version': '1.0',
    'author': "Skyscend Business Solutions Pvt. Ltd.",
    'category': 'Hotel',
    'depends': ['base'],
    'website': 'https://www.goibibo.com',
    'data': ['security/rooms_security.xml',
             'security/ir.model.access.csv',
             'views/menu.xml',
             'data/rooms_sequence.xml',
             'data/service_sequence.xml',
             'views/service_views.xml',
             'views/restaurant_views.xml',
             'wizard/wiz_update_mo_views.xml',
             'wizard/wiz_update_fields_views.xml',
             'wizard/wiz_update_m2m_view.xml',
             'wizard/wiz_update_m2o_view.xml',
             'views/rooms_views.xml',
             ],
    'assets': {
        'web.assets_backend': [
            'hotel/static/src/scss/hotel.scss'
        ]
    },

    'installable': True,
    'auto_install': False,
    'application': True

}

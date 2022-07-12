{
    'name': 'Car Rental inherit',
    'author': 'Jash Parikh',
    'description': "Practicing inheriting a module",
    'depends': ['base', 'car_rental'],
    'data': [
        # 'security/ir.model.access.csv',
        'view/checkout_inherit_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
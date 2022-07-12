{
    'name': 'Car Rental',
    'author': 'Jash Parikh',
    'description': "A basic car rental module",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/checkout_time_slots.xml',
        'wizard/book_ride_form.xml',
        'view/book_ride_view.xml',
        'view/car_rental_view.xml',
        'view/car_info_view.xml',
        'view/car_checkout_view.xml',
        'view/staff_data_view.xml',
        'menu/menu.xml',
        'report/booking_report_template.xml',
        'report/billing_report.xml',
        'report/report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
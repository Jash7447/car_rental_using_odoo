from odoo import fields, models, api


class CheckOutInherit(models.Model):
    #_name = "checkout_inherit"
    _inherit = "car.checkout"
    _description = "Car Checkout"

    booking_id = fields.Integer(string="booking id")

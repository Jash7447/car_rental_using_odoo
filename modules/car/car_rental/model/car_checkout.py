from odoo import api, fields, models


class CarCheckout(models.Model):
    _name = "car.checkout"
    _rec_name = "customer_name"

    @api.onchange('customer_name')
    def car_checkout_populate(self):
        for rec in self:
            self.customer_email = rec.customer_name.cus_email
            self.customer_city = rec.customer_name.cus_city
            self.customer_phone = rec.customer_name.cus_phone
            self.customer_age = rec.customer_name.cus_age
            self.fair = rec.customer_name.total_cost
            self.start_dt1 = rec.customer_name.ride_start_dt
            self.time_slot = rec.customer_name.checkout_time_slots
            self.end_date1 = rec.customer_name.ride_end_date
            self.booking_id = rec.customer_name.id
            self.car2 = rec.customer_name.car1

    customer_name = fields.Many2one("book.ride", string="Costumer name")
    customer_email = fields.Char(string="Email")
    customer_phone = fields.Char(string="Phone")
    customer_age = fields.Integer(string="Age")
    customer_city = fields.Selection(
        [('Ahmedabad', 'Ahmedabad'), ('Bangalore', 'Bangalore'), ('Mumbai', 'Mumbai'), ('Surat', 'Surat')],
        string="city",
        help="customer's city")
    start_dt1 = fields.Datetime(string="Check-out date")
    end_date1 = fields.Date(string="Check-in date")
    car2 = fields.Many2one("car.data", string="Car")
    fair = fields.Integer(string="fair", help="Total cost without tax.")
    time_slot = fields.Many2one("checkout.slots", string="Checkout time slot")


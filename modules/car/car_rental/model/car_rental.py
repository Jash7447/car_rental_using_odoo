from odoo import api, fields, models
from odoo.exceptions import ValidationError
# from datetime import datetime
# from collections import namedtuple
#from . import book_ride


class CarRental(models.Model):
    _name = "car.rental"
    _description = "Car Rental"
    _rec_name = "name"

    name = fields.Char(string="name", help="This is costumer name.",
                       required=True)

    email = fields.Char(string="Email", help="costumer email id")
    phone = fields.Char(string="phone", required=True, help="Enter your contact number.")
    age = fields.Integer(string="Age", default=18, help="Enter your age.")
    city = fields.Selection(
        [('Ahmedabad', 'Ahmedabad'), ('Bangalore', 'Bangalore'), ('Mumbai', 'Mumbai'), ('Surat', 'Surat')],
        string="city",
        required=True, help="Enter city")
    address = fields.Text(string="Address", help="Enter your address")
    # driver = fields.Boolean(string="Do you want to hire a driver?",
    #                         help="tick here if you want to hire a driver.")
    # start_dt = fields.Datetime(string="Start date and time", default=fields.Datetime.today(),
    #                            help="Enter date and time to start the trip.", required=True)
    # end_date = fields.Date(string="End date", default=fields.Date.today(), help="Enter date to end the trip.",
    #                        required=True)
    proof = fields.Image(string="valid proof(Adhar/licence)",
                         help="Upload a valid proof(Adhar/licence) here in image file format")
    status = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('cancel', 'Cancel')], default='draft')
    car = fields.Many2one("car.data", string="Car")
    cus_booking = fields.One2many("customer.bookings", "booking_id", string="Customer Bookings")
    bookings_count = fields.Integer(string="number of bookings of the customer", compute="get_booking_count")

    def get_booking_count(self):
        for rec in self:
            booking_count = self.env['book.ride'].search_count([('cus_name', '=', rec.name)])
            rec.bookings_count = booking_count


    @api.constrains('end_date')
    def _check_end_date(self):
        for record in self:
            if record.end_date < record.start_dt.date():
                raise ValidationError("Select a proper end date")

    @api.constrains('phone')
    def _phone_validation(self):
        for record in self:
            if len(record.phone) != 10:
                raise ValidationError("Phone number must be of 10 digits")
            if not (record.phone.isnumeric()):
                raise ValidationError("Phone number must only contain digits")

    def submit_action(self):
        self.status = "submitted"

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'

    def unlink(self):
        try:
            rtn = super(CarRental, self).unlink()
            return rtn
        except:
            raise ValidationError("Customer cannot be deleted.")

    def action_draft(self):
        self.status = 'draft'

    def action_submit(self):
        self.status = 'submitted'

    def action_open_bookings(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bookings',
            'res_model': 'book.ride',
            'domain': [('cus_name', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    # def unlink(self):
    #     print("self statement ", self)
    # for i in self:
    #     print("self statement>>>>>>>> ", i.name)

    # for profiles in self:
    #     print("selected name   >>>>>>>>>",profiles.name)
    #     check_profile = self.env['book.ride'].sudo().search(['name', '=', self.cus_name])
    #     print(">>>>>>>>>>>", check_profile)
    # if check_profile > 0:
    #     raise ValidationError("You cannot delete this user")
    # print(check_profile.cus_name)
    # if profiles.name == book_ride.cus_name:
    #     print(">>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<")
    # if check_profile>0:

    # rtn = super(CarRental, self).unlink()
    # print("Return statement ", rtn)
    # return rtn

    # class CarData(models.Model):
    #     _inherit = "car.data"
    #
    #     car_bookings = fields.One2many("car.rental", "car", string="Bookings")

    # def unlink(self):
    #     rtn = super(CarRental, self).unlink()
    #     for rec in self:
    #         print(">>>>>>>>>>>>>>>>>>>>>unlink_rec",rec.name)
    #         if rec.name:
    #             customer = self.env['book.ride'].sudo().search([('cus_name','=',rec.name)])
    #             print(">>>>>>>>>>>>>>>>>>>customer", customer.id)
    #             raise ValidationError("You cannot delete this user")
    #
    #     return rtn


class CustomerBookings(models.Model):
    _name = "customer.bookings"
    _description = "Customer Bookings"

    bookings = fields.Many2one('book.ride', string="bookings")
    booking_id = fields.Many2one('car.rental', string="booking id")

    driver_req1 = fields.Boolean(string="driver?",
                                 help="tick here if you want to hire a driver charges 1500/day.")
    sequence = fields.Integer(string="Sequence")
    ride_start_dt1 = fields.Date(string="Start date",
                                 help="Enter date and time to start the trip.")
    ride_end_date1 = fields.Date(string="End date", help="Enter date to end the trip.")
    car2 = fields.Many2one("car.data", string="Car")
    @api.onchange('bookings')
    def bookings_populate(self):
        for rec in self:
            self.driver_req1 = rec.bookings.driver_req
            self.ride_start_dt1 = rec.bookings.ride_start_dt
            self.ride_end_date1 = rec.bookings.ride_end_date
            self.car2 = rec.bookings.car1

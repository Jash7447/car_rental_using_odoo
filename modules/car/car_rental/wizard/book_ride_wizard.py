from odoo import api, fields, models
from odoo.exceptions import ValidationError
from collections import namedtuple


class BookRideWizard(models.Model):
    _name = "book.ride.wizard"

    name = fields.Many2one("book.ride", string="Costumer name")
    cus_name = fields.Many2one("car.rental", string="Costumer name", domain=[("status", "=", "submitted")],
                               required=True)
    cus_email = fields.Char(string="Email")
    cus_phone = fields.Char(string="Phone")
    cus_age = fields.Integer(string="Age")
    driver_req = fields.Boolean(string="driver?",
                                help="tick here if you want to hire a driver charges 1500/day.")

    ride_start_dt = fields.Date(string="Start date", default=fields.Datetime.today(),
                                help="Enter date and time to start the trip.", required=True)
    ride_end_date = fields.Date(string="End date", default=fields.Date.today(), help="Enter date to end the trip.",
                                required=True)
    checkout_time_slots = fields.Many2one("checkout.slots", string="Checkout Time Slot")
    car1 = fields.Many2one("car.data", string="Car", domain=[("car_status", "=", "working")], required=True)
    days_interval = fields.Integer(string="days", store=True)
    cost_per_day = fields.Integer(string="cost per day", store=True)
    total_cost = fields.Integer(string="Total charge", store=True)
    book_status = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('cancel', 'Cancel')], default='draft')
    ride_booked = fields.Boolean(string="Booked")

    @api.onchange('cus_name', 'car1')
    def car_checkout_populate(self):
        for rec in self:
            self.cus_email = rec.cus_name.email
            self.cus_phone = rec.cus_name.phone
            self.cus_age = rec.cus_name.age
            self.cost_per_day = rec.car1.rent_price
            print("customer email >>>>>>>>>>>>>>", self.cus_email)
            print("customer phone >>>>>>>>>>>>>>", self.cus_phone)
            print("customer age >>>>>>>>>>>>>>", self.cus_age)
            print("cost per day >>>>>>>>>>>>>", self.cost_per_day)

    # def car_checkout_populate

    @api.onchange('ride_start_dt', 'ride_end_date')
    def _date_difference(self):
        if self.ride_start_dt and self.ride_end_date:
            if self.ride_start_dt > self.ride_end_date:
                raise ValidationError('Donchangeate_in should not greater than Date_out.')
            # self.days_interval = 0
            if self.ride_start_dt < self.ride_end_date:
                day_calc = (self.ride_end_date - self.ride_start_dt).days
                self.days_interval = day_calc

    @api.onchange('days_interval', 'cost_per_day', 'driver_req')
    def _calculate_total(self):
        if self.days_interval == 0:
            if self.driver_req:
                self.total_cost = self.cost_per_day + 1500
            else:
                self.total_cost = self.cost_per_day
        else:
            if self.driver_req:
                self.total_cost = self.days_interval * (self.cost_per_day + 1500)
            else:
                self.total_cost = self.days_interval * self.cost_per_day

    @api.constrains('car1')
    def check_availability(self):
        same_car = self.env['book.ride'].sudo().search([('id', '!=', self.id)])
        print("whole record >>>>>>>>>>>>>>>", same_car)
        for rec in same_car:
            print("rec.car1rec.car1rec.car1", rec.car1)
            if rec.car1 == self.car1:
                # print(".....>>>>>>>>>>>>>>>>>>>>>..............<<<<<<<<<<<<<<<<<<<.....")
                date1_start = rec.ride_start_dt
                print('date1 start >>>>>>>>>>>', date1_start)
                date1_end = rec.ride_end_date
                print('date1 end >>>>>>>>>>>', date1_end)
                Range = namedtuple('Range', ['start', 'end'])
                r1 = Range(start=date1_start, end=date1_end)
                r2 = Range(start=self.ride_start_dt, end=self.ride_end_date)
                latest_start = max(r1.start, r2.start)
                earliest_end = min(r1.end, r2.end)
                delta = (earliest_end - latest_start).days + 1
                print("delta >>>>>>>>>>>", delta, end="\n")
                overlap = max(0, delta)
                print("overlap >>>>>>>>>>>", overlap, end="\n")
                if overlap != 0:
                    raise ValidationError("Selected car is not available please select another.")

    def create_booking(self):
        print("button is clicked")

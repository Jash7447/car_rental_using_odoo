from odoo import api, fields, models
from odoo.exceptions import ValidationError
from collections import namedtuple
from datetime import datetime


class BookRide(models.Model):
    _name = "book.ride"
    _rec_name = "cus_name"

    cus_name = fields.Many2one("car.rental", string="Costumer name", domain=[("status", "=", "submitted")],
                               required="TRUE")
    cus_email = fields.Char(string="Email")
    cus_phone = fields.Char(string="Phone")
    cus_age = fields.Integer(string="Age")
    driver_req = fields.Boolean(string="driver?",
                                help="tick here if you want to hire a driver charges 1500/day.", default=True)

    ride_start_dt = fields.Date(string="Start date", default=fields.Datetime.today(),
                                help="Enter date and time to start the trip.", required=True)
    ride_end_date = fields.Date(string="End date", help="Enter date to end the trip.",
                                required=True)
    checkout_time_slots = fields.Many2one("checkout.slots", string="Checkout Time Slot")
    car1 = fields.Many2one("car.data", string="Car", domain=[("car_status", "=", "working")],
                           required="TRUE")
    # days = fields.Integer(string="days", compute='_date_difference')
    days_interval = fields.Integer(string="days", store=True)
    cost_per_day = fields.Integer(string="cost per day")
    cost_per_day1 = fields.Integer(string="cost per day")
    total_cost = fields.Integer(string="Total charge", store=True)
    book_status = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('cancel', 'Cancel')], default='draft')
    ride_booked = fields.Boolean(string="Booked")
    cus_address = fields.Text(string="Customer Address", help="Enter your address")
    cus_city = fields.Selection(
        [('Ahmedabad', 'Ahmedabad'), ('Bangalore', 'Bangalore'), ('Mumbai', 'Mumbai'), ('Surat', 'Surat')],
        string="city",
        required=True, help="Enter city")
    car_brand = fields.Selection(
        [('Maruti Suzuki', 'Maruti Suzuki'), ('Honda', 'Honda'), ('Hyundai', 'Hyundai'), ('Skoda', 'Skoda'),
         ('Ford', "Ford"), ('Tata', 'Tata'), ('Toyota', 'Toyota'), ('Renault', 'Renault'), ('Mahindra', 'Mahindra'),
         ('Kia', 'Kia')])
    car_type1 = fields.Selection([('hatchback', 'Hatchback'), ('sedan', 'Sedan'), ('suv', 'SUV'), ('muv', 'MUV')],
                                 string="Car type",
                                 help="Enter city")
    tax_on_product = fields.Integer(string="tax", store=True)
    price_after_tax = fields.Integer(string="net price", store=True)
    date_today = fields.Date(string="Today date", default=fields.Datetime.today())
    booking_count = fields.Integer(string="Total bookings", compute='get_booking_count')
    # deadline_date = fields.Datetime(string="Remaining days")

    # def get_booking_count(self):
    #     for rec in self:
    #         booking_count = self.env['book.ride'].search_count([('id', '=', rec.id)])
    #         rec.booking_count = booking_count

    @api.onchange('cus_name', 'car1')
    def car_checkout_populate(self):
        for rec in self:
            self.cus_email = rec.cus_name.email
            self.cus_phone = rec.cus_name.phone
            self.cus_age = rec.cus_name.age
            self.cus_address = rec.cus_name.address
            self.cus_city = rec.cus_name.city
            self.cost_per_day = rec.car1.rent_price
            self.cost_per_day1 = rec.car1.rent_price
            self.car_brand = rec.car1.brand
            self.car_type1 = rec.car1.car_type

            print("customer email >>>>>>>>>>>>>>", self.cus_email)
            print("customer phone >>>>>>>>>>>>>>", self.cus_phone)
            print("customer age >>>>>>>>>>>>>>", self.cus_age)
            print("cost per day >>>>>>>>>>>>>", self.cost_per_day)

    # def car_checkout_populate
    # def get_appointment_count(self):
    #     count = self.env['hospital.appointment'].search_count([('id', '=', self.id)])
    #     self.appointment_count = count


    @api.onchange('ride_start_dt', 'ride_end_date')
    def _date_difference(self):
        if self.ride_start_dt and self.ride_end_date:
            if self.ride_start_dt > self.ride_end_date:
                raise ValidationError('Date_in should not greater than Date_out.')
            # self.days_interval = 0
            if self.ride_start_dt < self.ride_end_date:
                day_calc = (self.ride_end_date - self.ride_start_dt).days
                self.days_interval = day_calc

    @api.onchange('days_interval', 'total_cost', 'cost_per_day1', 'cost_per_day', 'driver_req', 'car1')
    def _calculate_total(self):
        # car_name = self.car1
        if self.days_interval == 0:
            if self.driver_req:
                self.cost_per_day1 = self.cost_per_day + 1500
                self.total_cost = self.cost_per_day1
                self.car_checkout_populate()
                # print("111111111111111111111111", self.cost_per_day, self.cost_per_day1, self.total_cost)
            else:
                self.cost_per_day1 = self.cost_per_day
                self.total_cost = self.cost_per_day1
                # print("222222222222222222222222", self.cost_per_day, self.cost_per_day1, self.total_cost)
        else:
            if self.driver_req:
                # print("333333333333333333333333", self.cost_per_day, self.cost_per_day1, self.total_cost)
                self.cost_per_day1 = self.cost_per_day + 1500
                self.total_cost = self.days_interval * self.cost_per_day1
                # print("333333333333333333333333", self.cost_per_day, self.cost_per_day1, self.total_cost)
            else:
                # print("444444444444444444444444", self.cost_per_day, self.cost_per_day1, self.total_cost)
                self.cost_per_day1 = self.cost_per_day
                self.total_cost = self.days_interval * self.cost_per_day1
                # print("444444444444444444444444", self.cost_per_day, self.cost_per_day1, self.total_cost)

        self.car_checkout_populate()

        # self.car1 = car_name

        self.tax_on_product = self.total_cost * 0.15
        self.price_after_tax = self.total_cost + self.tax_on_product
        # print(">>>>>>>>>>>>>>", self.tax_on_product, self.price_after_tax)

    # @api.depends('ride_end_date')
    # def _date_difference(self):
    #     print(">>>>>>>>>>>>")
    #
    #     if self.ride_start_dt and self.ride_end_date:
    #         if self.ride_start_dt.date() > self.ride_end_date:
    #             raise ValidationError('Date_in should not greater than Date_out.')
    #         self.days_interval = 0
    #         if self.ride_start_dt.date() < self.ride_end_date:
    #             day_calc = (self.ride_end_date - self.ride_start_dt.date()).days
    #             print(">>>>>", day_calc)
    #             self.days_interval = day_calc

    # def date_overlap(self,d1s,d1e):
    #     Range = namedtuple('Range', ['start', 'end'])
    #     r1 = Range(start=d1s, end=d1e)
    #     r2 = Range(start=self.ride_end_date, end=self.ride_end_date)
    #     latest_start = max(r1.start, r2.start)
    #     earliest_end = min(r1.end, r2.end)
    #     delta = (earliest_end - latest_start).days + 1
    #     overlap = max(0, delta)
    #     return overlap
    #
    # @api.constrains('car1')
    # def _check_availability(self):
    #     car_unavailable = self.env['book.ride'].search(
    #         [('car1', '=', 'self.car1'), ('date_overlap(ride_start_dt, ride_end_date)', '!=', '0')]
    #     )

    @api.constrains('car1')
    def check_availability(self):
        same_car = self.env['book.ride'].sudo().search([('id', '!=', self.id)])
        print("whole record >>>>>>>>>>>>>>>", same_car)
        for rec in same_car:
            print("rec.car1rec.car1rec.car1", rec.car1)
            if rec.car1 == self.car1:
                # print(".....>>>>>>>>>>>>>>>>>>>>>..............<<<<<<<<<<<<<<<<<<<.....")
                date1_start = rec.ride_start_dt
                # print('date1 start >>>>>>>>>>>', date1_start)
                date1_end = rec.ride_end_date
                # print('date1 end >>>>>>>>>>>', date1_end)
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

    def submit_action(self):
        self.book_status = "submitted"

    def action_cancel(self):
        self.book_status = 'cancel'

    def action_draft(self):
        self.book_status = 'draft'

    @api.model
    def create(self, values):
        print('create values >>', values)
        values['ride_booked'] = True
        values['book_status'] = 'submitted'
        rtn = super(BookRide, self).create(values)
        print('return value of create is >>', rtn)
        return rtn

    def write(self, values):
        print('write values >>', values)
        values['ride_booked'] = True
        rtn = super(BookRide, self).write(values)
        print('return value of create is >>', rtn)
        return rtn

    def unlink(self):
        if self.book_status not in ('draft', 'cancel'):
            raise ValidationError("Cannot delete submitted bookings")
        rtn = super(BookRide, self).unlink()
        return rtn

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):

        rec = super(BookRide, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                               orderby=orderby, lazy=lazy)
        if 'cus_age' in fields:
            for lines in rec:
                lines['cus_age'] = False
        return rec


class CheckoutSlots(models.Model):
    _name = "checkout.slots"
    _rec_name = "time_slots"
    time_slots = fields.Char(string="Time Slots")


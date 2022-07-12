from odoo import api, fields, models


class CarData(models.Model):
    _name = "car.data"
    _rec_name = "car_name"

    car_name = fields.Char(string="Car name", required=True)
    car_type = fields.Selection([('hatchback', 'Hatchback'), ('sedan', 'Sedan'), ('suv', 'SUV'), ('muv', 'MUV')],
                                string="Car type",
                                help="Enter city")
    seat = fields.Integer(string="Seats")
    brand = fields.Selection(
        [('Maruti Suzuki', 'Maruti Suzuki'), ('Honda', 'Honda'), ('Hyundai', 'Hyundai'), ('Skoda', 'Skoda'),
         ('Ford', "Ford"), ('Tata', 'Tata'), ('Toyota', 'Toyota'), ('Renault', 'Renault'), ('Mahindra', 'Mahindra'),
         ('Kia', 'Kia')])
    photo = fields.Image(string="Photograph")
    rent_price = fields.Integer(string="Rent price per day")
    car_status = fields.Selection(
        [('working', 'working'), ('under_maintenance', 'Under Maintenance'), ('not_available', 'Not Available')],
        default='working')
    car_bookings_count = fields.Integer(string="number of bookings of the customer", compute="get_car_booking_count")

    def get_car_booking_count(self):
        for rec in self:
            booking_count = self.env['book.ride'].search_count([('car1', '=', rec.car_name)])
            rec.car_bookings_count = booking_count


    def working_action(self):
        self.car_status = 'working'

    def maintenance_action(self):
        self.car_status = 'under_maintenance'

    def action_not_available(self):
        self.car_status = 'not_available'

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s %s [%s]' % (field.brand, field.car_name, field.car_type)))
        return res

    def action_open_car_bookings(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bookings',
            'res_model': 'book.ride',
            'domain': [('car1', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    # @api.model
    # def _name_search(self, name='', args=None, operator='ilike', limit=50):
    #     if args is None:
    #         args = []
    #     domain = args + ['|', ('name', operator, name), ('car_name', operator, name)]
    #     return super(CarData, self).search(domain, limit=limit).name_get()

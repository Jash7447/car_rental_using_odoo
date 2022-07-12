from odoo import api, fields, models
from odoo.exceptions import ValidationError

class StaffData(models.Model):
    _name = "staff.data"
    _rec_name = "name"

    flag = False
    name = fields.Char(string="name", help="This is costumer name.",
                       required=True)

    email = fields.Char(string="Email", help="costumer email id")
    phone = fields.Char(string="phone", required=True, help="Enter your contact number.")
    age = fields.Integer(string="Age", default=18, help="Enter your age.")
    city = fields.Selection(
        [('Ahmedabad', 'Ahmedabad'), ('Bangalore', 'Bangalore'), ('Mumbai', 'Mumbai'), ('Surat', 'Surat')],
        string="city",
        required=True, help="Enter city")
    role = fields.Selection(
        [('manager', 'Manager'), ('driver', 'Driver'), ('accounting', 'Accounting'), ('mechanic', 'Mechanic')],
        string="Role",
        required=True, help="select a role")
    proof = fields.Binary(string="valid proof(Adhar/licence)",
                         help="Upload a valid proof(Adhar/licence). "
                              "Would be considered at the time of reviewing your profile.")
    status = fields.Selection(
        [('cancel', 'Cancel'), ('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved')],
        default='draft')

    # @api.onchange('proof')
    # def ChangeFlag(self):
    #     print(">>>>>>>>>>>>proof>>>>>>>>", self.proof)
    #     self.proof = 'proof'
    #     self.flag = True
    #     print(">>>>>>>>>>>>proof>>>>>>>>", self.proof)

    @api.model
    def create(self, values):
        if values['proof']:
            values['status'] = 'submitted'
        # else:
        #     raise ValidationError("Your profile won't be submitted for verification until you attach an proof")
        print(">>>>proof>>>>", values['proof'])
        rtn = super(StaffData, self).create(values)
        print('return value of create is >>', rtn)
        return rtn

    def write(self, values):
        if values['proof']:
            values['status'] = 'submitted'
        rtn = super(StaffData, self).write(values)
        return rtn

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
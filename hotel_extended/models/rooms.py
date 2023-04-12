from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Room(models.Model):
    _inherit = ['hotel.rooms', 'mail.activity.mixin', 'mail.thread']
    _name = 'hotel.rooms'
    # _rec_name= 'city'

    blood_group = fields.Selection([('a_n', 'A-ve'),
                                    ('a_p', 'A+ve'),
                                    ('b_n', 'B-ve'),
                                    ('b_p', 'B+ve'),
                                    ('ab_n', 'AB-ve'),
                                    ('ab_p', 'AB+ve'),
                                    ('o_n', 'O-ve'),
                                    ('o_p', 'O+ve')], 'Blood Group', tracking=True)

    # restaurant_id = fields.Many2one('hotel.restaurant', string='ordered food', tracking=True)
    address = fields.Text(string='Address')
    feedbacks = fields.Text(string='coustomer_review')
    marital_stautus = fields.Selection([('single', 'Single'), ('married', 'Married')], 'Marital Status')
    state = fields.Selection(selection_add=[('welcome', 'Welcome')], tracking=True)
    # amenity_ids = fields.One2many('hotel.service', 'amenity_type_id', 'amenity')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.uid)

    def print_hello(self):
        print("---HELLO----")

        # To call the parent method
        super().print_hello()

    @api.onchange('name', 'age')
    def _computeVar(self):
        res = super()._computeVar()
        for record in self:
            if record.name:
                email = record.name + '@111' + 'gmail.com'
                record.email = email
        return res

    @api.constrains('mo_no')
    def check_name(self):
        res1 = super().check_name
        for room in self:
            if len(room.mo_no) > 10:
                raise ValidationError('make sure that the length of a mo_no field is exactly 10 characters.!')

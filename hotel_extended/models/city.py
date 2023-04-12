from odoo import models,fields
class City(models.Model):
    _inherit = ['hotel.restaurant','hotel.service']
    _name = 'hotel.city'
    _description = 'Cities'
    _auto = True
    # _rec_name = 'cities'
    cities = fields.Text("Cities")

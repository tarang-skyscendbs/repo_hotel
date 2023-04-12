from odoo import models,fields,api
class Service(models.Model):
    _name = 'hotel.service'
    _description = 'Service'
    _auto = True
    _rec_name = 'service'
    room_id = fields.Many2one('hotel.rooms', string='CustomerName')
    service = fields.Selection(selection=[('Carrental services','carrental services'),('Catering services','catering services'),('Courier services',
'courier services'),('Doctor on call','doctor on call'),('Dry cleaning','dry cleaning')],string='Services')
    rent = fields.Float(string='Rent', digits=(16, 3), group_operator='avg')
    service_charge = fields.Float(string='Service charge')
    food_charge = fields.Float(string='Food Charge')
    customer_code = fields.Char("C_code")
    color = fields.Integer('Color Index')
    city_id = fields.Many2one('hotel_extended.rooms',string='city')

    @api.model_create_multi
    def create(self, vals_lst):
        for vals in vals_lst:
            vals.update({
                'customer_code': self.env['ir.sequence'].next_by_code('hotel.service')
            })
        return super().create(vals_lst)

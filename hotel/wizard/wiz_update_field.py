from odoo import models,fields
class UpdateField(models.TransientModel):
    _name='wiz.update.field'
    room_id = fields.Many2one('hotel.rooms', string='CustomerName')
    service = fields.Selection(
        selection=[('Carrental services', 'carrental services'), ('Catering services', 'catering services'),
                   ('Courier services',
                    'courier services'), ('Doctor on call', 'doctor on call'), ('Dry cleaning', 'dry cleaning')],
        string='Services')
    customer_code = fields.Char("C_code")
    color = fields.Integer('Color Index')
    restaurant_id = fields.Many2one('hotel.restaurant', string='ordered food')
    city_id = fields.Many2one('hotel_extended.rooms', string='city')
    def update_field(self):
        print("Cstmr", self.room_id)
        room = self.room_id
        print('------',room)
        room_ids = self.room_id.ids
        if not room_ids:
            room_obj = self.env['hotel.rooms']
            print("ACTIVE IDDSSSSSS", self.env.context['active_ids'])
            room_ids = self.env.context['active_ids']
            room = room_obj.browse(room_ids)
        room.write({'service_id':[(0,0,{'color':self.color,'service':self.service,'customer_code':self.customer_code})]})


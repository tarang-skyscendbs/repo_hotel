from odoo import models,fields
class UpdateField(models.TransientModel):
    _name='wiz.update.m2o'
    room_id = fields.Many2one('hotel.rooms', string='CustomerName')
    restaurant_id = fields.Many2one('hotel.restaurant', string='ordered food')


    def update_field_m2o(self):
        print("Cstmr", self.room_id)
        room = self.room_id
        print('------', room)
        room_ids = self.room_id.ids
        if not room_ids:
            room_obj = self.env['hotel.rooms']
            print("ACTIVE IDDSSSSSS", self.env.context['active_ids'])
            room_ids = self.env.context['active_ids']
            room = room_obj.browse(room_ids)
        room.write({'room_ids':self.room_ids})

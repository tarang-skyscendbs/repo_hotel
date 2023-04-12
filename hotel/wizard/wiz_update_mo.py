from odoo import models,fields


class UpdateAge(models.TransientModel):
    _name='wiz.update.mo'
    room_id = fields.Many2one('hotel.rooms', string='CustomerName')
    mobile = fields.Char('mo_no')

    def update_mo(self):
        print("Cstmr", self.room_id)
        room = self.room_id
        print('------',room)
        room_ids = self.room_id.ids
        if not room_ids:
            room_obj = self.env['hotel.rooms']
            print("ACTIVE IDDSSSSSS", self.env.context['active_ids'])
            room = room_obj.browse(room_ids)
        room.write({'mo_no':self.mobile})



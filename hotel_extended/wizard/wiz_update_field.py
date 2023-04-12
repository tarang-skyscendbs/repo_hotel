from odoo import models,fields
class UpdateField(models.TransientModel):
    _inherit = 'wiz.update.field'
    room_id = fields.Many2one('hotel.rooms', string='CustomerName')
    id_proof = fields.Selection(
        [('Aadhar', 'aadhar'), ('Pan-card', 'pan-card'), ('Driving-Licence', 'driving-licence')])

    def update_field(self):
        print("Cstmr", self.room_id)
        room = self.room_id
        print('------', room)
        room_ids = self.room_id.ids
        if not room_ids:
            room_obj = self.env['hotel.rooms']
            print("ACTIVE IDDSSSSSS", self.env.context['active_ids'])
            room_ids = self.env.context['active_ids']
            room = room_obj.browse(room_ids)
        room.write({'id_proof': self.id_proof})
        return super().update_field()
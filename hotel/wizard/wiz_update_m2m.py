from odoo import models,fields
class UpdateFieldm2m(models.TransientModel):
    _name='wiz.update.m2m'
    serve_ids = fields.Many2many('hotel.restaurant', string='your order')
    # room_id = fields.Many2one('hotel.rooms', string='CustomerName')


    def update_m2m(self):
        print("Cstmr", self.room_id)
        room = self.room_id
        print('------',room)
        room_ids = self.room_id.ids
        print(room_ids)
        if not room_ids:
            room_obj = self.env['hotel.rooms']
            print("ACTIVE IDDSSSSSS", self.env.context['active_ids'])
            room_ids = self.env.context.get('active_ids')
            room = room_obj.browse(room_ids)

    def open(self):
        room_ids = self.serve_ids.ids
        print("======", room_ids)

        if len(room_ids) == 1:
            # If one record it will open a form view.
            return {
                'name': 'Menu',
                'type': 'ir.actions.act_window',
                'view_mode': 'form,tree',
                'res_model': 'hotel.restaurant',
                'res_id': room_ids[0]
            }
        else:
            # If multiple records it will open a tree view.
            return {
                'name': 'Menu',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'hotel.restaurant',
                'domain': [('id', 'in', room_ids)],
            }

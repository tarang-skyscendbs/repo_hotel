from odoo import models,fields

class RoomAnalysis(models.Model):
    _name='rooms.analysis'
    _auto=False

    name = fields.Char(string='Name')
    customer_code = fields.Char("C_code")
    room_type = fields.Selection(selection=[('delux', 'Delux'), ('single', 'Single'), ('double', 'Double')],
                                 string='Room_type')
    email = fields.Char('Email')
    room_id = fields.Many2one('hotel.rooms', string='CustomerName')
    age = fields.Integer(string='Age', group_operator='max')


    def init(self):
        # self.env.cr.execute("""create or replace view rooms_analysis as
        # (SELECT  r.id ,s.room_id,s.customer_code, r.room_type , r.email from hotel_service s , hotel_rooms r where s.room_id=r.id)""")


        self.env.cr.execute("""create or replace view rooms_analysis as
        (SELECT  r.id , s.room_id, s.customer_code ,r.age, r.room_type , r.email from hotel_service s , hotel_rooms r where r.id=s.room_id)""")
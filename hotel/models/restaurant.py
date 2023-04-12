from odoo import models,fields,api
class Restaurant(models.Model):
    _name = 'hotel.restaurant'
    _description = 'Restaurant'
    _auto = True
    _rec_name= 'order'
    name_of_rest = fields.Char('name')
    room_id = fields.Many2one('hotel.rooms', string='CustomerName')
    # order = fields.Selection([('Breakfasts', 'breakfasts'),('Brunch', 'brunch'),('Afternoon and High Tea Menu', 'Afternoon and High Tea Menu')])
    order = fields.Selection([('Fruit & nut breakfast bowl', 'fruit & nut breakfast bowl'), ('Vegan strawberry pancakes.', 'vegan strawberry pancakes'),
                              ('Banana & tahini porridge.', 'banana & tahini porridge.')])

    order_code = fields.Char('Code', size=4)
    color = fields.Integer('Color Index')

    @api.model_create_multi
    def create(self,vals_lst):
        for vals in vals_lst:
            print("Vals_Lst",vals_lst)
            if not vals.get('order_code', False):
                vals['order_code'] = vals['order'][:4].upper()
                print("UPDATED VALS", vals)
        return super().create(vals_lst)
    #
    def write(self,vals):
        print("vals",vals)
        for restaurant in self:
            if not restaurant.order_code or ('order_code' in vals and not vals.get('order_code')):
                if vals.get('order'):
                    vals['order_code'] = vals['order'][:4].upper()
                else:
                    vals['order_code'] = restaurant.order[:4].upper()
        print("UPDATE VALS", vals)
        return super().write(vals)

    def name_get(self):

        lst = []
        for res in self:
            order = res.order
            if res.order_code:
                name = '<' + res.order_code + '> ' + order
            lst.append((res.id,name))
        return lst

    @api.model
    def name_search(self, name='', args=[], operator='ilike', limit=100):

        if name:
            args += ['|', ('order', operator, name), ('order_code', operator, name)]
        s = self.search(args, limit=limit)
        return s.name_get()

    @api.model
    def name_create(self, order):
        if self._rec_name:
            vals = {
                self._rec_name: order,
                'order_code': order[:2].upper() + order[-1:]
            }
            record = self.create(vals)
            return record.name_get()[0]
        else:
            return False


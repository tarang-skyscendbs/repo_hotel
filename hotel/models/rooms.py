from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime




class Room(models.Model):
    _name = 'hotel.rooms'
    _description = 'Room'
    _auto = True
    _order = 'name'

    # , domain = [('order', 'like', 'it')]
    # , domain = [('order', 'like', '%ts')]
    restaurant_id = fields.Many2one('hotel.restaurant', string='ordered food')
    # partner_id = fields.Many2one('res.partner', 'Contact')


    serve_ids = fields.Many2many('hotel.restaurant', string='your order')
    ref = fields.Reference([('res.users', 'Users'), ('res.partner', 'Partners'), ('hotel.rooms', 'Customers')],
                           'Reference')
    service_id = fields.One2many('hotel.service', 'room_id', string='Service_')
    # menu_id = fields.One2many('hotel.restaurant', 'room_id', string='Service_food', limit=2)
    state = fields.Selection([('check-in', 'Checkin'),
                              ('stay-in', 'Stay-in'),
                              ('check-out', 'Check-out'), ], 'State', default='stay-in')
    name = fields.Char(string='Name')
    age = fields.Integer(string='Age', group_operator='max')
    mo_no = fields.Char('Phone_number')
    room_code = fields.Char('room_code')
    checkin_date = fields.Date(string='Checkin', index=True)
    checkout_date = fields.Date('Checkout')
    birth_date = fields.Date('Birthdate')
    room_type = fields.Selection(selection=[('delux', 'Delux'), ('single', 'Single'), ('double', 'Double')],
                                 string='Room_type')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender')
    reference = fields.Char(string='reference', size=20)
    payment = fields.Boolean('Payment')
    pwd = fields.Char('Password')
    rating = fields.Selection([('Disgusting', 'disgusting'), ('poor', 'Poor'), ('average', 'Average'), ('good', 'Good'),
                               ('excellent', 'Excellent')])
    email = fields.Char('Email')
    website = fields.Char('Website')
    total_hours = fields.Float('Total Hours')
    feedback = fields.Text('Feedback', translate=True)
    cleaning = fields.Boolean('Cleaning', default=True)
    housekeeping = fields.Boolean('Housekeeping', default=True)
    template = fields.Html('Template')
    id_proof = fields.Selection(
        [('Aadhar', 'aadhar'), ('Pan-card', 'pan-card'), ('Driving-Licence', 'driving-licence')])
    document = fields.Binary('Document')
    file_name = fields.Char('File Name')
    img = fields.Image('Image')
    total_charges = fields.Float(compute='_calc_total_charges', string='Total Charges', store=True)
    total_charges1 = fields.Float(compute='_calc_total_charges', string='Total charges(excluding food bill)',
                                  store=True)
    per = fields.Float(compute='_calc_percentage')
    sequence = fields.Integer(string='Sequence')
    _parent_store = True
    _parent_name = 'parent_id'
    parent_id = fields.Many2one('hotel.rooms', 'Main', store=True)
    child_ids = fields.One2many('hotel.rooms', 'parent_id', 'Sub')
    parent_path = fields.Char('Parent Path', index=True)
    # update_user_id = fields.Many2one('res.users', 'Update_user')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.uid)

    # the color field is used to indicate colors for the record
    # It must be an integer field and should be used with widget color_picker
    color = fields.Integer('Color Index')

    @api.depends('service_id.rent', 'service_id.service_charge', 'service_id.food_charge')
    def _calc_total_charges(self):
        print("HOTEL(SELF)", self)
        for rooms in self:
            total_charges = 0
            total_charges1 = 0
            for total in rooms.service_id:
                total_charges = total.rent + total.service_charge + total.food_charge
                total_charges1 = total.rent + total.service_charge - total.food_charge

            rooms.total_charges = total_charges
            rooms.total_charges1 = total_charges1

    @api.depends('total_charges', 'total_charges1')
    def _calc_percentage(self):
        for rooms in self:
            per = 0.0
            if rooms.total_charges:
                per = rooms.total_charges1 * 100 / rooms.total_charges
            rooms.per = per

    def customer_checkin(self):
        for rooms in self:
            rooms.state = 'stay-in'

    def customer_stayin(self):
        for rooms in self:
            rooms.state = 'check-out'

    def customer_checkout(self):
        for rooms in self:
            rooms.state = 'check-in'

    def print_hello(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Hello",self)
        print("Environment------->", self.env)
        print("Obj------->", self.env['hotel.rooms'].search([('user_id', '=', self.user_id.id)]))
        print("ARGS", self.env.args)
        print("Language", self.env.lang)
        print("User", self.env.user)
        print("Company", self.env.company)
        # print("CONTEXT", self.env.context)
        print("current_user_id", self.env.uid)
        print("")

        all_rooms = self.search([])
        print("-------", all_rooms)
        new = all_rooms.mapped(lambda n1: (str(n1.name) + "-" + str(n1.age)))
        print('iiiii', new)
        m = all_rooms.get_metadata()
        print("Metadata", m)
        f1 = all_rooms.filtered(lambda x: x.id_proof == 'Aadhar')
        print("Filtered data based on condition", f1)
        f3 = all_rooms.filtered(lambda x: x.id_proof == 'Pan-card')
        print("Filtered data based on condition", f3)
        u1 = f1 | f3
        print("union of ID_PROOF is", u1)
        i1 = f1 & f3
        print("intersection of f1&f3 is", i1)
        d1 = all_rooms - f3
        print("difffrence btn allrooms and f3 is", d1)

        f2 = all_rooms.filtered(lambda x: x.room_type == 'double')
        print("Filtered data based on condition", f2)
        f1_set = f1 < all_rooms
        print("f1 is subset of all_rooms?", f1_set)
        f2_set1 = f2 < all_rooms
        print("f2 is subset of all_rooms?", f2_set1)
        all_rooms_set = all_rooms > f1
        print("all_rooms is superset of f1?", all_rooms_set)
        all_rooms_set1 = all_rooms > f2
        print("all_rooms is superset of f2?", all_rooms_set1)
        m1 = all_rooms.mapped('room_type')
        print('records which do have a value in the field should be displayed.', m1)
        m2 = all_rooms.mapped(lambda x1: (x1.age, x1.id_proof))
        print('records which do have a value in the field should be displayed.', m2)
        sorted_by_age = all_rooms.sorted(key='age', reverse=True)
        print("sorted_by_age", sorted_by_age)
        view_rec = self.env.ref('hotel.view_rooms_search')
        print("View Record", view_rec)

    def create_new_record(self):
        vals_list = []
        vals1 = {
            'name': 'Xyz',
            'age': 25,
            'gender': 'male',
            'checkin_date': fields.Date.today(),
            'menu_id': [(0, 0, {'room_id': 'Xyz',
                                'order': 'Brunch'
                                })]}

        vals_list.append(vals1)
        rooms1 = self.create(vals_list)
        print("create a new record", rooms1)

    def update_exixting_record(self):
        for rooms in self:
            vals = {
                'name': 'Riya',
                'age': 26,
                'service_id': [
                    # (0,0,{
                    #     'room_id':'Tarang',
                    #     'service':'Dry cleaning'}),
                    # # (2,5)
                    # (3,2)]}
                    (3, 1)]}

            # 'serve_id':[(3,1)]}

            rooms.write(vals)

    def update(self):
        for rooms in self:
            vals = {
                'name': 'Riya',
                'age': 44}
            rooms.write(vals)

    def search_record(self):
        all_r = self.search([])
        print("All rooms", all_r)

        all_r_sk_2 = self.search([], offset=2)
        print("record after skipping", all_r_sk_2)
        all_r_sk_3 = self.search([], offset=2, order='name')
        print("record after skipping based on condition", all_r_sk_3)
        a1 = self.search([('age', '=', 25)])
        print("search by age", a1)
        no_of_rooms = self.search([], count=True)
        print('No of rooms', no_of_rooms)
        # subordinates = self.search([('id', 'child_of', 4), ('id', '!=', 4)])
        # print("SUBORDINATES", subordinates)

    def search_count_record(self):
        no_of_rooms = self.search_count([("gender", "=", "female")])
        print("---------", no_of_rooms)

    def read_record(self):
        record = self.read()
        print("READ RECORD", record)
        all_rooms = self.search([])
        record = all_rooms.read(fields=['name', 'age', 'restaurant_id'], load='')
        print("READ RECORD OF M20", record)

    def search_read_record(self):
        res = self.search_read(fields=['name', 'age', 'gender', 'room_type'], order='name', limit=4)
        print("result of search read record is", res)
        res1 = self.search_read([('gender', '=', 'female')])
        print("search read record", res1)
        all_records = self.search([])
        print("record set of current user ", all_records)

    no_of_services = fields.Integer('No of services', compute='_count_services')
    no_of_food_items = fields.Integer('No of food_items', compute='_count_food_items')

    def _count_services(self):
        room_obj = self.env['hotel.service']
        print("no of services in perticular room", room_obj)
        for room in self:
            room.no_of_services = room_obj.search_count([('room_id', '=', room.id)])

    def _count_food_items(self):
        room_obj = self.env['hotel.restaurant']
        print("no of services in perticular room", room_obj)
        for room in self:
            room.no_of_food_items = room_obj.search_count([('room_id', '=', room.id)])

    @api.model_create_multi
    def update_user(self):
        for room in self:
            # vals1 = {'update_user_id': self.env.uid}
            # print("---", vals1)
            # room.write(vals1)

            print(dir(self))
            print(self._uid)
            user_obj = self.env['res.users']
            print(user_obj.browse(self._uid))

    def copy(self, default=None):
        default = {'name': self.name + ' (Copy)', 'age': 28}
        return super().copy(default=default)

    def default_get(self, fields_list):
        result = super().default_get(fields_list=fields_list)
        result.update({'age': 8})
        print("RESULT", result)
        return result

    @api.model_create_multi
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        print("VIEW ID", view_id)
        print("VIEW TYPE", view_type)
        print("TOOLBAR", toolbar)
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        field_attr = res.get('fields').get('age', {})
        if field_attr:
            res['fields']['age'].update({'readonly': True})
            print(res['fields']['age'])
        print("FIELDS VIEW GET RESULT", res)
        return res

    #
    @api.onchange('birth_date')
    def onchange_birthday(self):
        """
        When birthdate is changed it should change the age
        --------------------------------------------------
        :param self: object pointer
        """
        for room in self:
            if room.birth_date:
                age = int(((fields.Date.today() - room.birth_date).days) / 365)
                room.age = age

    # @api.onchange('checkin_date', 'checkout_date','total_hours')
    # def calculate_date(self):
    #     if self.checkin_date and self.checkout_date:
    #         d1=datetime.strptime(str(self.checkin_date),'%Y-%m-%d')
    #         d2=datetime.strptime(str(self.checkout_date),'%Y-%m-%d')
    #         d3=(d2-d1)*24
    #         self.total_hours=str(d3.days)
    #













    # @api.onchange('total_hours','checkin_date','checkout_date')
    # def onchange_total_hours(self):
    #     for room in self:
    #         total_hours=0
    #         if room.checkin_date:
    #             total_hours=str(((room.checkout_date - room.checkin_date).days)*24)
    #             room.total_hours = total_hours
    #             print("Total hours",total_hours)
    #         # else:
    #             return {
    #                 'warning': {
    #                     'title': 'warning',
    #                     'message': 'IIIIIIIIIIIIII'}
    #             ,
    #             'domain': {
    #             'restaurant_id': ['|', ('order', 'ilike', 'br'), ('order', 'ilike', 'bre')]}}
    #

    # _sql_constraints = [
    #     ('unique_order', 'unique(mo_no)', 'The code of the order must be unique!'),
    #     ('check_age', 'check(age>18)', 'Age must be greater than 18!'),
    # ]

    @api.constrains('name')
    def check_name(self):
        for room in self:
            if len(room.name) > 6:
                raise ValidationError('make sure that the length of a character field is exactly 6 characters.!')

    @api.model_create_multi
    def create(self, vals_lst):
        for vals in vals_lst:
            vals.update({
                'room_code': self.env['ir.sequence'].next_by_code('hotel.rooms')

            })
        return super().create(vals_lst)

    # @api.depends("payment","food_qty")
    # def _compute_description(self):
    #     print('----self------',self.food_qty)
    #     self.totalbill = self.payment * self.food_qty

    @api.onchange('name')
    def _computeVar(self):
        for record in self:
            if record.name:
                email = record.name + '@' + 'gmail.com'
                record.email = email

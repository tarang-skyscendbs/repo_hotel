from odoo import models, fields, api


class BikeTemplate(models.Model):
    _name = 'bike.template'
    _rec_name = 'model_name'

    model_name = fields.Char('Model Name')
    engine = fields.Char('Engine')
    bike_type = fields.Selection([('road bikes', 'Road bikes'),
                                 ('mountain bikes', 'Mountain bikes'),
                                 ('sport Bikes', 'Sport Bikes'),], 'Bike Type')


class Bike(models.Model):
    _name = 'bike.variant'

    # To use delegate inheritance you must have a many2one field of the parent
    # The many2one must have delegate=True which confirms the delegate inheritance.
    # The many2one field must be required
    # The many2one field also must have ondelete='cascade'
    # You can have multiple parents as well but you need to create separate many2one fields for each parent
    template_id = fields.Many2one('bike.template', delegate=True, required=True, ondelete='cascade')
    name = fields.Char('Name')
    fuel_type = fields.Selection([('petrol', 'Petrol'),
                                  ('electric', 'Electric')], 'Fuel Type')
    color = fields.Integer('Color')


class Bike2(models.Model):
    _name = 'bike.variant2'
    # This is another way of using delegation inheritance.
    # This is an older way and may get deprecated in the future versions
    # Here also you can use multiple parents. Each parent would be key to the dictionary.
    # The value to the key would be a many2one field to the parent
    _inherits = {'bike.template':'template_id'}

    template_id = fields.Many2one('bike.template', required=True, ondelete='cascade')
    name = fields.Char('Name')
    fuel_type = fields.Selection([('petrol', 'Petrol'),
                                  ('electric', 'Electric')], 'Fuel Type')
    color = fields.Integer('Color')

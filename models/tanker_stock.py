from odoo import models, fields

class TankerStock(models.Model):
    _name = 'tanker.stock'

    tanker_id = fields.Many2one(string="Tanker ID", comodel_name="fuel.tanker")
    fuel_categ = fields.Many2one(comodel_name="fuel.category")
    fuel_unit = fields.Char(string="Fuel Unit", related='fuel_categ.unit', store=True)

    capacity = fields.Float(string="Storage Capacity")
    used_capacity = fields.Float(string="Used Capacity")
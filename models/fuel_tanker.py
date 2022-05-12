from email.policy import default
from odoo import models, fields

class FuelTanker(models.Model):
    _name = 'fuel.tanker'

    name = fields.Char(string="Tanker ID")
    regitration_no = fields.Char(string="Tanker registration Number")
    description = fields.Char(string='Record Description')

    tanker_stock_ids = fields.One2many(string="Tanker Stock Ids", comodel_name="tanker.stock", inverse_name="tanker_id")

    source = fields.Char(string="Tanker Source")
    destination = fields.Char(string="Tanker Destination")
    state = fields.Selection([('ordered','Ordered'),
                              ('outForDelivery','Out For Delivery'),
                              ('delivered','Delivered'),
                              ('cancelled','Cancelled')], default="ordered", string="Status")
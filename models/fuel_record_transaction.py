from odoo import models, fields

class FuelRecordTransaction(models.Model):
    _name = 'fuel.record.transaction'

    name = fields.Char(string='Test Name')


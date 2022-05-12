from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FuelStock(models.Model):
    _name = 'fuel.stock'

    sub_station_name = fields.Many2one(comodel_name='fuel.station',string="Sub Station")
    fuel_catg = fields.Many2one(comodel_name='fuel.category', string='Fuel Category')

    fuel_price = fields.Float(string="Price Per Unit")
    fuel_unit = fields.Char(string="Fuel Unit", related='fuel_catg.unit', store=True)

    # @api.constrains('fuel_catg','sub_station_name')
    # def _check_existing_stock(self):
    #     temp_dict = {}
    #     for row in self:
    #         print(row)
        #     temp_dict[row.sub_station_name.name] = list()
        # print(temp_dict)
        # for row in self:
        #     if row.fuel_catg.name in temp_dict[row.sub_station_name.name]:
        #         raise ValidationError("Stock Already Exist!, Try updating existing Fuel Stock.")
        #     else:
        #         temp_dict[row.sub_station_name.name].append(row.fuel_catg.name)
        #         print(temp_dict[row.sub_station_name.name])

    _sql_constraints = [
        ('fuel_catg', 'unique(sub_station_name, fuel_catg)', "Stock with this Fuel Category already exist !"),
    ]


    capacity = fields.Float(string="Storage Capacity")

    record_in_ids = fields.One2many(comodel_name="fuel.record.in", inverse_name="stock_id", string="In Records")
    record_out_ids = fields.One2many(comodel_name="fuel.record.out", inverse_name="stock_id", string="Out Records")

    @api.depends("record_in_ids.fuel_volume","record_out_ids.fuel_volume")
    def _calc_usedCapacity(self):
        for stock_row in self:
            total_used_cap = 0
            for in_record in stock_row.record_in_ids:
                total_used_cap += in_record.fuel_volume
            for out_record in stock_row.record_out_ids:
                total_used_cap -= out_record.fuel_volume
            stock_row.used_capacity = total_used_cap

    used_capacity = fields.Float(string="Used Capacity", compute="_calc_usedCapacity", store=True, readonly=False)

    @api.depends("used_capacity")
    def _calc_emptyCapacity(self):
        for record in self:
            record.empty_capacity = record.capacity - record.used_capacity
            print("Setting empty capacity", record.empty_capacity)

    empty_capacity = fields.Float(string="Empty capacity", compute="_calc_emptyCapacity", store=True)
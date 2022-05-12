from odoo import models, fields, api

class FuelStation(models.Model):
    _name = 'fuel.station'
    # _inherit = 'product.template'

    name = fields.Char(string='Fuel Station Name')
    address = fields.Char(string='Location of the station')

    stock_ids = fields.One2many(comodel_name='fuel.stock', inverse_name='sub_station_name', string="Stock Ids")

    # capacity = fields.Float(string="Storage Capacity")

    # record_in_ids = fields.One2many(comodel_name="fuel.record.in", inverse_name="sub_station_name", string="In Records")
    # record_out_ids = fields.One2many(comodel_name="fuel.record.out", inverse_name="sub_station_name", string="Out Records")

    # @api.depends("record_in_ids.fuel_volume","record_out_ids.fuel_volume")
    # def _calc_usedCapacity(self):
    #     for station_record in self:
    #         total_used_cap = 0
    #         for in_record in station_record.record_in_ids:
    #             total_used_cap += in_record.fuel_volume
    #         for out_record in station_record.record_out_ids:
    #             total_used_cap -= out_record.fuel_volume
    #         station_record.used_capacity = total_used_cap

    # used_capacity = fields.Float(string="Used Capacity", compute="_calc_usedCapacity", store=True, readonly=False)

    # @api.depends("used_capacity")
    # def _calc_emptyCapacity(self):
    #     for record in self:
    #         record.empty_capacity = record.capacity - record.used_capacity
    #         print("Setting empty capacity", record.empty_capacity)

    # empty_capacity = fields.Float(string="Empty capacity", compute="_calc_emptyCapacity", store=True)

    @api.depends("stock_ids.record_in_ids.total_cost_price","stock_ids.record_out_ids.total_selling_price")
    def _calc_capital(self):
        for station_row in self:
            temp_capital = 0
            for stock_row in station_row.stock_ids:
                # compute capital after IN record created
                # for in_record in stock_row.record_in_ids:
                #     temp_capital -= in_record.total_cost_price

                for out_record in stock_row.record_out_ids:
                    temp_capital += out_record.total_selling_price

            station_row.capital = temp_capital

    capital = fields.Float(string="Total Capital", compute="_calc_capital", store=True)

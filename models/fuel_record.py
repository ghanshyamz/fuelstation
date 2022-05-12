from pickletools import float8
from tkinter.tix import Tree
from odoo.exceptions import ValidationError
from odoo import api, models, fields
from odoo.tools.float_utils import float_compare, float_is_zero

class FuelRecordIn(models.Model):
    _name = 'fuel.record.in'

    description = fields.Char(string='Record Description')
    
    sub_station_name = fields.Many2one(comodel_name='fuel.station')
    # ss_stoc_ids 

    fuel_categ = fields.Many2one(comodel_name="fuel.category")

    @api.depends('fuel_categ','sub_station_name')
    def _compute_stock_id(self):
        for row in self:
            temp_id = None
            for id in row.sub_station_name.stock_ids:
                print("Stock id: ",id)
                if row.fuel_categ == id.fuel_catg:
                    temp_id = id
            row.stock_id = temp_id

    stock_id = fields.Many2one(comodel_name='fuel.stock', compute="_compute_stock_id")

    @api.constrains('stock_id','fuel_catg','sub_station_name')
    def _check_stock_id(self):
        for record in self:
            if not record.stock_id:
                raise ValidationError("Selected Stock is NOT available!")

    capacity = fields.Float(string="Total Capacity", related='stock_id.capacity', store=True)
    
    fuel_volume = fields.Float(string="Fuel Volume")
    record_date = fields.Datetime(string="Record Date and Time")

    @api.depends('fuel_categ','sub_station_name')
    def _get_price_per_unit(self):

        self.cost_price_per_unit = self.stock_id.fuel_price
        print("cost per unit", self.cost_price_per_unit)

    cost_price_per_unit = fields.Float(string="Cost Price Per Unit", compute="_get_price_per_unit", store=True)
    
    @api.depends('fuel_categ','sub_station_name','cost_price_per_unit','stock_id','fuel_volume')
    def _get_total_price(self):
        self.total_cost_price = self.stock_id.fuel_price * self.fuel_volume
    
    total_cost_price = fields.Float(string="Total Cost Price", compute="_get_total_price", store=True, readonly=True)
    seller = fields.Char(string="Seller's Name")

    @api.constrains('fuel_volume','empty_cap')
    def _check_fuel_volume(self):
        for record in self:
            if float_is_zero(record.fuel_volume, precision_digits=4):
                raise ValidationError("Fuel volume can't be zero")
            elif record.empty_cap < 0:
                print("Difference : ",record.fuel_volume,record.empty_cap)
                raise ValidationError("Not enough fuel capacity")

    empty_cap = fields.Float(string="Empty Capacity", related='stock_id.empty_capacity', store=True)
    # tanker = fields.Many2one(comodel_name='fuel.tanker',string='Tanker')


############################## RECORD OUT ##############################################
class FuelRecordOut(models.Model):
    _name = 'fuel.record.out'

    description = fields.Char(string='Record Description')

    sub_station_name = fields.Many2one(comodel_name='fuel.station', string='Sub Station')
    fuel_categ = fields.Many2one(comodel_name="fuel.category")
    
    
    @api.depends('fuel_categ','sub_station_name')
    def _compute_stock_id(self):
        for row in self:
            temp_id = None
            for id in row.sub_station_name.stock_ids:
                print("Stock id: ",id)
                if row.fuel_categ == id.fuel_catg:
                    temp_id = id
            row.stock_id = temp_id
    
    stock_id = fields.Many2one(comodel_name='fuel.stock', compute="_compute_stock_id")

    @api.constrains('stock_id','fuel_catg','sub_station_name')
    def _check_stock_id(self):
        for record in self:
            if not record.stock_id:
                raise ValidationError("Selected Stock is NOT available!")

    avl_stock = fields.Float(string="Available Stock", related='stock_id.used_capacity')

    @api.constrains('fuel_volume','avl_stock')
    def _check_fuel_volume(self):
        for record in self:
            if float_is_zero(record.fuel_volume, precision_digits=4):
                raise ValidationError("Fuel volume can't be zero")
            elif record.avl_stock < 0:
                print(record.avl_stock, record.fuel_volume)
                raise ValidationError("Not enough Fuel Stock")

    fuel_volume = fields.Float(string="Fuel Volume")
    record_date = fields.Datetime(string="Record Date and Time")

    @api.depends('fuel_categ','sub_station_name')
    def _get_price_per_unit(self):
        self.selling_price_per_unit = self.stock_id.fuel_price

    selling_price_per_unit = fields.Float(string="Selling Price Per Unit", compute="_get_price_per_unit", store=True)
    
    @api.depends('fuel_categ','sub_station_name','selling_price_per_unit','stock_id','fuel_volume')
    def _get_total_price(self):
        self.total_selling_price = self.stock_id.fuel_price * self.fuel_volume
    
    total_selling_price = fields.Float(string="Total Selling Price", compute="_get_total_price", store=True, readonly=True)
    
    buyer = fields.Char(string="Buyer's Name")
    
    # tanker = fields.Many2one(comodel_name='fuel.tanker',string='Tanker used')

class FuelCategory(models.Model):
    _name = 'fuel.category'

    name = fields.Char(string="Fuel Category")
    unit = fields.Char(string="Fuel Unit")
    # price = fields.Float(string="Fuel Price")
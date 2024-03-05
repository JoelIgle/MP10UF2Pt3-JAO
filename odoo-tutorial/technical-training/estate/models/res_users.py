from odoo import fields, models
class User(models.Model):
    """ This class extends the user object with some properties"""
    _inherit = "res.users"
    property_ids = fields.One2many("estate.property","salesperson_id","Propietats")
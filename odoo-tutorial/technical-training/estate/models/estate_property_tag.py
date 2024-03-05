from odoo import fields, models 

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Model per estate.property.tag"
    name = fields.Char('Etiqueta', required=True)
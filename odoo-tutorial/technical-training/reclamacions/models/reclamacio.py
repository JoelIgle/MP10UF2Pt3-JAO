from odoo import models, fields
class Reclamacio(models.Model):
    _name = 'reclamacio'
    name = fields.Char('Nom', required=True)


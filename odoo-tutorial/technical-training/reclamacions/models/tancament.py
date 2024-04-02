from odoo import models, fields

class Tancament(models.Model):
    _name = 'tancament'
    name = fields.Char('Nom')

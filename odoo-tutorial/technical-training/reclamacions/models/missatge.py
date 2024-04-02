from odoo import models, fields, api

class Missatge(models.Model):
    _name = 'missatge'
    name = fields.Text('Missatge')
    creator_id = fields.Many2one('res.partner', string='Creador missatge', required=True)
    reclamacio_id = fields.Many2one('reclamacio', "Reclamacio")


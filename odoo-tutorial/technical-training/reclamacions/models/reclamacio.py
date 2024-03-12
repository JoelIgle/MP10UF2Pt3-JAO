from odoo import models, fields
from datetime import datetime
class Reclamacio(models.Model):
    _name = 'reclamacio'
    name = fields.Char('Nom', required=True)
    client_id = fields.Many2one('res.partner', string='Client que reclama')
    creator_id = fields.Many2one('res.users', string='Usuari que crea reclamació', default=lambda self: self.env.user.id)
    creation_date = fields.Date('Data de creació', copy=False, default=lambda self: datetime.today().date())
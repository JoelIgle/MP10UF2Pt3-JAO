from odoo import models, fields
from datetime import datetime
class Missatge(models.Model):
    _name = 'missatge'
    creator_id = fields.Many2one('res.users', string='Usuari que crea reclamació', default=lambda self: self.env.user.id)
    creation_date = fields.Date('Data de creació', copy=False, default=lambda self: datetime.today().date())
    message_body = fields.Text('Missatge')

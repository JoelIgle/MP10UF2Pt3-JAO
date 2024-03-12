from odoo import models, fields
from datetime import datetime

class Reclamacio(models.Model):
    _name = 'reclamacio'
    name = fields.Char('Nom', required=True)
    client_id = fields.Many2one('res.partner', string='Client que reclama')
    creator_id = fields.Many2one('res.users', string='Usuari que crea reclamació', default=lambda self: self.env.user.id)
    creation_date = fields.Date('Data de creació', copy=False, default=lambda self: datetime.today().date())

    sale_order_id = fields.Many2one('sale.order', string='Comanda de vendes asociada')
    description = fields.Text('Descripció')

    modification_date = fields.Date('Data de modificació', copy=False, default=lambda self: datetime.today().date())
    closing_date = fields.Date('Data de tancament', copy=False, default=lambda self: datetime.today().date())
    
    MOTIUS_TANCAMENT = [
        ('resolt', 'Resolt'),
        ('cancel·lat', 'Cancel·lat'),
        ('altre', 'Altres'),
    ]

    # Camp per al motiu de tancament o cancel·lació
    reason_for_closing = fields.Selection(MOTIUS_TANCAMENT, string='Motiu de Tancament o Cancel·lació')

from odoo import models, fields, api
from datetime import datetime

class Reclamacio(models.Model):
    _name = 'reclamacio'
    name = fields.Char('Nom', required=True)
    client_id = fields.Many2one('res.partner', string='Client que reclama', required=True)
    creator_id = fields.Many2one('res.users', string='Usuari que crea reclamació', readonly=True, default=lambda self: self.env.user.id)
    # order_id = fields.Many2one('sale.order', string='Comanda de vendes asociada')
    closing_date = fields.Date('Data de tancament', copy=False, default=lambda self: datetime.today().date())
    tancament = fields.Selection([
        ('resolt', 'Resolt'),
        ('cancel·lat', 'Cancel·lat'),
        ('altre', 'Altres')
        ], string='Motiu de Tancament o Cancel·lació')
    description = fields.Text('Descripció')
    

    # Aquí afegeix Aleix

    estat = fields.Selection([('New','Nova'), ('In treatment', 'En tractament'), ('Closed', 'Tancada'), ('Canceled', 'Cancel·lada'), ],default='New')

    @api.onchange('estat')
    def canvi_estat(self):
        if self.estat == 'Closed':
            self.closing_date = datetime.today().date()

    # Aquí acaba el d'Aleix

    # Aquí afegeix Joel


    # Aquí acaba el de Joel

    # Aquí afegeix Oriol



    # Aquí acaba el d'Oriol



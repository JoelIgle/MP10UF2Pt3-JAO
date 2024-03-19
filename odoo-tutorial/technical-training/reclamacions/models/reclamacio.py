from odoo import models, fields, api
from datetime import datetime

class Reclamacio(models.Model):
    _name = 'reclamacio'
    name = fields.Char('Nom', required=True)
    client_id = fields.Many2one('res.partner', string='Client que reclama', required=True)
    creator_id = fields.Many2one('res.users', string='Usuari que crea reclamació', readonly=True, default=lambda self: self.env.user.id)
    sales_order_id = fields.Many2one('sale.order', string='Comanda de vendes asociada')
    closing_date = fields.Date('Data de tancament', copy=False, default=lambda self: datetime.today().date())
    tancament = fields.Selection([
        ('resolt', 'Resolt'),
        ('cancel·lat', 'Cancel·lat'),
        ('altre', 'Altres')
        ], string='Motiu de Tancament o Cancel·lació')
    missatges = fields.One2many('missatge', 'reclamacio_id', string='Missatges')

    # Aquí afegeix Aleix

    estat = fields.Selection([('New','Nova'), ('In treatment', 'En tractament'), ('Closed', 'Tancada'), ('Canceled', 'Cancel·lada'), ],default='New')

    @api.onchange('estat')
    def tanco_estat(self):
        if self.estat == 'Closed':
            self.closing_date = datetime.today().date()

    @api.onchange('missatges')
    def canvi_estat(self):
        if self.missatges.__len__()>=1:
            self.estat == 'In treatment'
    

    # Aquí acaba el d'Aleix

    # Aquí afegeix Joel
    initial_description = fields.Text('Descripció inicial de la reclamació')
    final_description = fields.Text('Una descripció de la resolució final de la reclamació')

    # Aquí acaba el de Joel

    # Aquí afegeix Oriol



    # Aquí acaba el d'Oriol



from odoo import models, fields, api
from datetime import datetime

class Reclamacio(models.Model):
    _name = 'reclamacio'
    _description = 'Reclamación'

    name = fields.Char('Nom', required=True)
    client_id = fields.Many2one('res.partner', string='Client que reclama', required=True)
    creator_id = fields.Many2one('res.users', string='Usuari que crea reclamació', readonly=True, default=lambda self: self.env.user.id)
    sales_order_id = fields.Many2one('sale.order', string='Comanda de vendes asociada')
    closing_date = fields.Date('Data de tancament', copy=False, default=lambda self: datetime.today().date())
    tancament_id = fields.Many2one('tancament', string='Motiu de Tancament o Cancel·lació')
    missatges = fields.One2many('missatge', 'reclamacio_id', string='Missatges')
    estat = fields.Selection([('New', 'Nova'),('Open','Oberta'), ('In treatment', 'En tractament'), ('Closed', 'Tancada'), ('Canceled', 'Cancel·lada'), ],default='New')

    initial_description = fields.Text('Descripció inicial de la reclamació')
    final_description = fields.Text('Una descripció de la resolució final de la reclamació')

    # Restricción de unicidad en el campo 'name'
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'El nom de la reclamació ha de ser únic.'),
    ]

    # Restricción sobre los valores permitidos en el campo 'estat'
    @api.constrains('estat')
    def _check_estat_values(self):
        for record in self:
            allowed_values = ['Open', 'In treatment', 'Closed', 'Canceled']
            if record.estat and record.estat not in allowed_values:
                raise models.ValidationError("El valor de l'estat no és vàlid.")

    # Restricción sobre los valores permitidos en el campo 'tancament_id'
    @api.constrains('tancament_id')
    def _check_tancament_id_values(self):
        for record in self:
            allowed_tancament_ids = [1, 2, 3]  # Lista de IDs permitidos para 'tancament_id'
            if record.tancament_id and record.tancament_id.id not in allowed_tancament_ids:
                raise models.ValidationError("El valor de Motiu de Tancament o Cancel·lació no és vàlid.")

    # Restricción personalizada para controlar reclamaciones "abiertas" asociadas a la misma comanda en el mismo momento
    @api.constrains('sales_order_id')
    def _check_duplicate_open_reclamacions(self):
        for record in self:
            if record.estat == 'Open' and record.sales_order_id:
                duplicate_reclamacions = self.search([('id', '!=', record.id), ('estat', '=', 'Open'), ('sales_order_id', '=', record.sales_order_id.id)])
                if duplicate_reclamacions:
                    raise models.ValidationError("Ja hi ha una reclamació oberta associada a aquesta comanda.")
                    
    @api.onchange('missatges')
    def _onchange_missatges(self):
        if self.missatges:
            self.estat = 'In treatment'
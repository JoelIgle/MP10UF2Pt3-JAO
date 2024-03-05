from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model per estate.property.offer"
    price = fields.Float('Preu', default=0.0, required=True, help='Preu ofertat per la propietat')
    status = fields.Selection([('Accepted', 'Acceptada'), ('Refused', 'Rebutjada'), ('draft', 'En Tractament')],
                              string='Estat', default='draft', copy=False)
    comments = fields.Text('Comentaris')
    partner_id = fields.Many2one('res.partner', string='Comprador', required=True)
    property_id = fields.Many2one('estate.property', string='Propietat', required=True)

    

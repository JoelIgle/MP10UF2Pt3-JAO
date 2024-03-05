from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Propietat Immobiliària'
        
    name = fields.Char('Propietat Immobiliària', required=True)
    description = fields.Text('Descripció')
    postcode = fields.Char('Codi Postal', required=True)
    date_availability = fields.Date('Data de disponibilitat', copy=False, default=lambda self: (fields.Date.today() + timedelta(days=30)))
    expected_price = fields.Float('Preu esperat', digits=(12, 2), currency_field='currency_id', default=0.0)
    selling_price = fields.Monetary('Preu de venda', compute='accept_offer', currency_field='currency_id', search=True, default=0.0, help='Preu de venda de la propietat')
    best_offer = fields.Monetary('Millor oferta', currency_field='currency_id', compute='_compute_best_offer', store=True, readonly=True)
    bedrooms = fields.Integer('Nombre d\'habitacions', required=True)
    state = fields.Selection([
        ('New', 'Nou'),
        ('Offer Received', 'Oferta Rebuda'),
        ('Offer Accepted', 'Oferta Acceptada'),
        ('Sold', 'Venuda'),
        ('Canceled', 'Cancel·lada')
    ], string="Estat", default='New', copy=False, required=True)
    active = fields.Boolean('Actiu', default=False, invisible=True)
    elevator = fields.Boolean('Ascensor', default=False)
    parking = fields.Boolean('Aparcament', default=False)
    renovated = fields.Boolean('Renovat', default=False)
    bathroom = fields.Integer('Nombre de banys')
    surface = fields.Integer('Superfície', required=True)
    construction_year = fields.Integer('Any de construcció')
    energy_certificate = fields.Char('Certificat energètic')
    price_m2 = fields.Float('Preu per metre quadrat', compute='_calcular_preu_m2', readonly=True, currency_field='currency_id')
    buyer_id = fields.Many2one('res.partner', compute='accept_offer', default=lambda self: self.env.user.id, string='Comprador')
    
    salesperson_id = fields.Many2one('res.users', string='Comercial', default=lambda self: self.env.user.id)
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
    offer_ids = fields.One2many('estate.property.offer','property_id', string='Ofertes')
    property_type_id = fields.Many2one('estate.property.types', string='Tipus')


    @api.depends('offer_ids.status', 'offer_ids.price', 'offer_ids.partner_id')
    def accept_offer(self):
        for prop in self:
            # Filtrar las ofertes que han sigut acceptades
        
            accepted_offers = prop.offer_ids.filtered(lambda offer: offer.status == 'Accepted')
            if accepted_offers:
                # Agafarà la primera oferta acceptada
                accepted_offer = accepted_offers[0]
                prop.buyer_id = accepted_offer.partner_id
                prop.selling_price = accepted_offer.price
            else:
                # Per a que no done error, ja que al intentar crear no hi haura cap oferta acceptada
                prop.buyer_id = False
                prop.selling_price = 0.0

    @api.depends('offer_ids.price', 'offer_ids.status')
    def _compute_best_offer(self):
        for prop in self:
            # Filtrar las ofertes que no estan refusades
            accepted_offers = prop.offer_ids.filtered(lambda offer: offer.status != 'Refused')
            if accepted_offers:
                # Calcular la oferta amb el preu més alt
                prop.best_offer = max(accepted_offers.mapped('price'))
            else:
                prop.best_offer = 0.0

    @api.depends('expected_price', 'surface')
    def _calcular_preu_m2(self):
        for prop in self:
            if prop.surface != 0:
                prop.price_m2 = prop.expected_price / prop.surface
            else:
                prop.price_m2 = 0.0
                
    @api.constrains('selling_price','expected_price')
    def _check_selling_price_vs_expected(self):
        for record in self:
            if record.selling_price < record.expected_price*0.9:
                raise ValidationError("El preu de venda no pot ser inferior al 90% del preu esperat")
        
    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_new_or_canceled(self):
        if any(property.state not in ([ 'New', 'Canceled']) for property in
        self):
            raise UserError("No es pot eliminar una propietat que no és nova o cancel·lada") 
    
    @api.model
    def create(self, vals):

        """ Crea una oferta i canvia estat de la propietat """
        offer = super().create(vals)
        offer.property_id.state = 'Offer Received'
        return offer
        
    # Aquí definim les restriccions            
    _sql_constraints = [
        ('check_positive_expected_selling_price',
        'CHECK(expected_price >= 0)',
        'El preu esperat ha de ser positiu.'),
        
        ('name_uniq', 'unique(name)', 'El nom de la propietat ha de ser únic.'),
        ]

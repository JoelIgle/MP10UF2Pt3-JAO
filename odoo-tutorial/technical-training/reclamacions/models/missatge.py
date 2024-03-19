from odoo import models, fields, api
class Missatge(models.Model):
    _name = 'missatge'
    creator_id = fields.Many2one('res.partner', string='Creador missatge', required=True)
    message_body = fields.Text('Missatge')
    finished = fields.Boolean("Acabat", default=False)
    reclamacio_id = fields.Many2one('reclamacio', "Reclamacio")

@api.onchange('finished')
def _canvi_finished(self):
    if self._canvi_finished():
        self.ensure_one()
        self.creator_id.readonly=True
        self.message_body.readonly=True

from odoo import models, fields, api


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(
        string="Disease Name",
        required=True,
        help="The name of the disease",
    )

    type = fields.Selection(
        selection=[
            ('infectious', 'Infectious Disease'),
            ('neurological', 'Neurological Disorder'),
            ('cardiovascular', 'Cardiovascular Disease'),
            ('oncological', 'Oncological Disease'),
            ('genetic', 'Genetic Disorder'),
            ('autoimmune', 'Autoimmune Disease'),
            ('mental', 'Mental Health Disorder'),
            ('other', 'Other') ,
        ],
        string='Disease Type',
        required=True,
        help="Category or type of the disease."
    )

    complete_name = fields.Char(
        compute='_compute_complete_name',
        recursive=True,
        store=True,
    )

    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Disease',
        index=True,
        ondelete='cascade',
        help="Parent category this disease belongs to, used for hierarchy",
    )

    parent_path = fields.Char(
        index=True,
        unaccent=False,
    )

    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases',
        help="Subcategories or more specific diseases under this category",
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for rec in self:
            if rec.parent_id:
                rec.complete_name = '%s / %s' % (
                    rec.parent_id.complete_name, rec.name)
            else:
                rec.complete_name = rec.name

    @api.depends_context('hierarchical_naming')
    def _compute_display_name(self):
        if self.env.context.get('hierarchical_naming', True):
            super()._compute_display_name()
            return
        for record in self:
            record.display_name = record.name

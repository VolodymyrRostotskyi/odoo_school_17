
from odoo import models, fields


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.person.mixin'
    _description = 'Doctor'

    specialty = fields.Selection(
        selection=[
            ('gp', 'General Practitioner'),
            ('pediatrician', 'Pediatrician'),
            ('cardiologist', 'Cardiologist'),
            ('dermatologist', 'Dermatologist'),
            ('psychiatrist', 'Psychiatrist'),
        ],
        required=True,
        help="Medical specialty of the doctor",
    )

    is_intern = fields.Boolean(
        help="Check this box if the doctor is currently an intern under"
             " supervision"
    )

    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor',
        domain=[('is_intern', '=', False)],
        help="Mentor responsible for supervising the intern doctor",
    )

    intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id',
        string='Interns',
        help='List of intern doctors supervised by this doctor'
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    )

    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )

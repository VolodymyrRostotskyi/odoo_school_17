
from datetime import date

from odoo import models, fields, api


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = "hr.hospital.person.mixin"
    _description = 'Patient'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
    )

    birth_date = fields.Date(
        string="Date of Birth",
        help="Patient’s date of birth",
    )

    age = fields.Integer(
        compute="_compute_age",
        store=True,
        readonly=True,
        help="Patient’s current age, calculated from birth date"
    )

    tax_id_number = fields.Char(
        string='Tax ID Number',
        help='ID Card Number',
    )

    passport_number = fields.Char(
        help='National passport number',
    )

    passport_issuer = fields.Char(
        string='Issued By',
        help='Authority that issued the passport',
    )

    passport_issue_date = fields.Date(
        string='Date of Issue',
        help='Date the passport was issued',
    )

    emergency_contact_name = fields.Char(
        help="Full name of the person to contact in case of emergency"
    )

    emergency_contact_phone = fields.Char(
        help="Phone number of the emergency contact person"
    )

    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )

    @api.depends("birth_date")
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (
                        rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0

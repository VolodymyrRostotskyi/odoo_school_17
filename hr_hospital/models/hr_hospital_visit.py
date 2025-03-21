from odoo import models, fields


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'

    visit_date = fields.Date(
        string="Visit Date",
        required=True,
        default=fields.Datetime.now
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True
    )

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
    )

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
    )

    complaint = fields.Text(
        string="Complaint",
    )

    diagnosis = fields.Text(
        string="Diagnosis",
    )

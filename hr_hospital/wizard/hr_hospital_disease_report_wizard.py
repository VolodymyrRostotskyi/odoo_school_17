from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class HrHospitalDiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Monthly Disease Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
        help='Select one or more doctors. Leave empty to include all doctors'
             ' in the report.',
    )

    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
        help='Select one or more diseases. Leave empty to include all diseases'
             ' in the report.',
    )

    date_from = fields.Date(
        string='From Date',
        required=True,
        help='Start date of the reporting period.',
    )

    date_to = fields.Date(
        string='To Date',
        required=True,
        help='End date of the reporting period.',
    )

    @api.constrains('date_from', 'date_to')
    def check_actual_visit_datetime(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise ValidationError(_(
                    "End date cannot be earlier than start date."
                ))

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())  # понеділок
        end_of_week = start_of_week + timedelta(days=6)  # неділя

        res['date_from'] = start_of_week
        res['date_to'] = end_of_week
        return res

    def action_generate_report(self):
        self.ensure_one()

        domain = [
            ('create_date','>=',self.date_from),
            ('create_date','<=',self.date_to)
        ]

        if self.doctor_ids:
            domain.append(('doctor_id','in',self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id','in',self.disease_ids.ids))

        return {
            'name': _('Disease Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.diagnosis',
            'view_mode': 'tree',
            'target': 'current',
            'domain': domain,
        }


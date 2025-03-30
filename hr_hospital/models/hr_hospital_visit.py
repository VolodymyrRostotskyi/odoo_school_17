from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, time


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
        help="Patient attending the visit"
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        help="Doctor assigned to this visit"
    )

    status = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        required=True,
        default='scheduled',
        help="Select the current status of the patient visit",
    )

    scheduled_visit_datetime = fields.Datetime(
        string="Scheduled Date",
        required=True,
        default=fields.Datetime.now,
        help="Planned date of the patient's visit"
    )

    actual_visit_datetime = fields.Datetime(
        string="Actual Visit Date",
        help="The exact date and time when the visit took place"
    )

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses',
        help="Diagnoses made during this visit",
    )

    @api.model
    def write(self, vals):
        for rec in self:
            if rec.status == 'completed' and 'status' not in vals:
                locked_fields = ['scheduled_visit_datetime', 'doctor_id',
                                 'actual_visit_datetime']
                for field in locked_fields:
                    if field in vals:
                        raise ValidationError(_(
                            f"You cannot change '{field}' after the"
                            f" visit is completed."
                        ))
            if rec.diagnosis_ids and vals.get('active') is False:
                raise ValidationError(_(
                    "You cannot archive a visit that has one or more "
                    " diagnoses assigned."
                ))
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.diagnosis_ids:
                raise ValidationError(_(
                    "You cannot delete a visit that has one or more "
                    " diagnoses assigned."
                ))
        return super().unlink()

    @api.constrains('status')
    def check_actual_visit_datetime(self):
        for rec in self:
            if rec.status == 'completed' and not rec.actual_visit_datetime:
                raise ValidationError(_(
                    "Actual Visit Date must be set when the visit"
                    " status is 'Completed'."
                ))

    @api.constrains('patient_id',
                    'doctor_id',
                    'scheduled_visit_datetime')
    def _check_duplicate_visit_per_day(self):
        for rec in self:
            if not rec.patient_id or not rec.doctor_id or \
                    not rec.scheduled_visit_datetime:
                continue

            start_dt = datetime.combine(rec.scheduled_visit_datetime.date(),
                                        time.min)
            end_dt = datetime.combine(rec.scheduled_visit_datetime.date(),
                                      time.max)

            duplicates = self.search([
                ('id', '!=', rec.id),
                ('patient_id', '=', rec.patient_id.id),
                ('doctor_id', '=', rec.doctor_id.id),
                ('scheduled_visit_datetime', '>=',
                 fields.Datetime.to_string(start_dt)),
                ('scheduled_visit_datetime', '<=',
                 fields.Datetime.to_string(end_dt)),
            ])

            if duplicates:
                raise ValidationError(_(
                    "This patient already has a visit scheduled with this "
                    "doctor on that day."
                ))

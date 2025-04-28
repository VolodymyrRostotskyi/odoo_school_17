
from odoo import _, models, fields, api
from odoo.exceptions import ValidationError


class HrHospitalDiagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Patient diagnosis'

    description = fields.Text(
        string="Treatment Description",
        help="Instructions or notes related to the proposed treatment plan",
    )

    is_approved = fields.Boolean(
        string="Approved",
        help="Check if this diagnosis has been approved by a doctor or mentor",
    )

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
        help='Patient to whom this diagnosis is assigned',
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        help='Doctor who assigned this diagnosis',
    )

    is_doctor_intern = fields.Boolean(
        string="Doctor is Intern",
        compute="_compute_is_doctor_intern",
        readonly=True,
        help="Indicates whether the assigned doctor is an intern"
    )

    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor',
        help='Doctor responsible for approving the diagnosis of an intern',
        domain='[("is_intern", "=", False)]',
    )

    is_approved_by_mentor = fields.Boolean(
        string="Approved by Mentor",
        help="Confirmed by mentor for intern doctors",
    )

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string="Disease",
        required=True,
    )

    disease_type = fields.Selection(
        related='disease_id.type',
        string='Disease Type',
        store=True,
        readonly=True
    )

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Patient visits',
    )

    def _update_is_doctor_intern(self):
        for rec in self:
            rec.is_doctor_intern = rec.doctor_id.is_intern if \
                rec.doctor_id else False

    @api.depends('doctor_id')
    def _compute_is_doctor_intern(self):
        self._update_is_doctor_intern()

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):
        self._update_is_doctor_intern()

    @api.constrains('is_approved_by_mentor')
    def _check_is_approved_by_mentor(self):
        for rec in self:
            if rec.is_approved_by_mentor and not rec.mentor_id:
                raise ValidationError(_(
                    "Mentor must be specified when approval by mentor is set."
                ))

    @api.constrains('is_approved')
    def _check_is_approved(self):
        for rec in self:
            if rec.is_approved:
                if rec.is_doctor_intern and not rec.is_approved_by_mentor:
                    raise ValidationError(_(
                        "Interns must have mentor approval before diagnosis "
                        "can be marked as approved."
                    ))

    @api.depends('patient_id','disease_id','doctor_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.patient_id.name} - {record.disease_id.name} (Dr.{record.doctor_id.name}) [{record.create_date.strftime('%d.%m.%Y')}]"

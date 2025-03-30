from odoo import models, fields, api


class HrHospitalPatientWizard(models.TransientModel):
    _name = 'hr.hospital.patient.wizard'
    _description = 'Wizard to change doctor for selected patients'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        required=True,
        string="New Doctor",
        help="Select the new doctor for the patients",
    )

    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        help="Patients for whom the doctor will be updated",
    )

    def action_change_doctor(self):
        self.patient_ids.write({'doctor_id': self.doctor_id.id})

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['patient_ids'] = [(6, 0, self.env.context.get('active_ids', []))]
        return res


from odoo import models, fields


class HrHospitalPersonMixin(models.AbstractModel):
    _name = "hr.hospital.person.mixin"
    _description = "Abstract model with common personal information fields"

    name = fields.Char(
        string="Full Name",
        required=True,
        help="Enter the full name of the person (e.g., John Smith)",
    )

    phone = fields.Char(
        string="Phone Number",
        help="Enter the contact phone number (e.g., +1 234 567 8901)"
    )

    photo = fields.Image(
        max_width=512,
        max_height=512,
    )

    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other / Undefined')
        ],
        string="Gender",
        required=True,
        default='other',
        help="Select the gender of the person",
    )

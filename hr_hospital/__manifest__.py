{

    'name': 'Hospital Management',
    'summary': 'Manage doctors, patients, diagnoses and visits in a hospital environment',
    'author': 'Odoo School',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'license': 'OPL-1',
    'version': '17.0.2.0.0',
    'application': True,
    'images': [ ],
    'depends': [
        'base',
        'mail',
        'hr',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'security/ir.model.access.csv',

        'data/hr_hospital_disease_data.xml',

        'wizard/hr_hospital_patient_wizard_views.xml',

        'views/hr_hospital_menu.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_diagnosis_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_visit_views.xml',
    ],
    'demo': [
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
        'demo/hr_hospital_disease_demo.xml',
        'demo/hr_hospital_visit_demo.xml',
        'demo/hr_hospital_diagnosis_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}

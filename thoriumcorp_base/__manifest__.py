#
#    Copyright (C) 2020-2030 Thorium Corp FP <help@thoriumcorp.website>
#

{
    'name': 'Thorium Corp FP',
    'description': '''Adds Thoriumcorp Abstract Entity for Laboratories infraestructure''',
    'version': '13.0.0.0.1',
    'category': 'Thoriumcorp',
    'depends': [
        'base',
        'product',
        'base_locale_uom_default',
    ],
    'author': 'Thorium Corp FP',
    'website': 'http://thoriumcorp.website',
#    'license': 'GPL-3',
    'data': [
        'data/ir_sequence_data.xml',
        'data/thoriumcorp_specialty.xml',
        'security/thoriumcorp_security.xml',
        'security/ir.model.access.csv',
        # 'templates/assets.xml',
        'views/res_partner.xml',
        'views/thoriumcorp_abstract_entity.xml',
        'views/thoriumcorp_patient.xml',
        'views/thoriumcorp_menu.xml',
        'views/thoriumcorp_specialty.xml',
    ],
    'demo': [
        # 'demo/thoriumcorp_patient_demo.xml',
    ],
    'installable': True,
    'application': True,
    'maintainer': 'Julio César Méndez <mendezjcx@thoriumcorp.website>'
}

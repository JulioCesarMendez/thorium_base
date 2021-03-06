#
#    Copyright (C) 2020-2030 Thorium Corp FP <help@thoriumcorp.website>
#

from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char(
        string='CI',
        help='Personal Identity Card'
    )
    alias = fields.Char(
        string='Nickname',
        help='Common, not official, name'
    )
    patient_ids = fields.One2many(
        string='Related patients',
        comodel_name='thoriumcorp.patient',
        # compute='_compute_patient_ids_and_count',
        inverse_name='partner_id'
    )
    count_patients = fields.Integer(compute='_count_patients')
    birthdate_date = fields.Datetime(string='DOB')
    age = fields.Char('Age', help="Person's age")
    date_death = fields.Datetime('Time of death')
    deceased = fields.Boolean()
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        'Gender'
    )
    weight = fields.Float()
    weight_uom = fields.Many2one(
        string="Weight unit",
        comodel_name="uom.uom",
        default=lambda s: s.env['res.lang'].default_uom_by_category('Weight'),
        domain=lambda self: [(
            'category_id', '=',
            self.env.ref('uom.product_uom_categ_kgm').id)
        ])
    is_patient = fields.Boolean(
        string='Is patient?',
        help='Check if the partner is a patient'
    )
    unidentified = fields.Boolean(
        string='Unidentified',
        help='Patient is currently unidentified'
    )
    marital_status = fields.Selection(
        [
            ('s', 'Single'),
            ('m', 'Married'),
            ('w', 'Widow(er)'),
            ('d', 'Divorced'),
            ('x', 'Separated')
        ]
    )

    def _get_thoriumcorp_entity(self):
        self.ensure_one()
        if self.type and self.type[:7] == 'thoriumcorp':
            return self.env[self.type].search([
                ('partner_id', '=', self.id),
            ])

    def _count_patients(self):
        # TODO: Probar esto con pacientes asignados
        for record in self:
            try:
                patients = False
                # patients = self.env['thoriumcorp.patient'].search([
                #     ('partner_id', 'child_of', record.id),
                # ])[0]
                if patients:
                    print(76)
                    record.count_patients = len(patients)
                else:
                    record.count_patients = 0
            except Exception as e:
                print(78, e)
                record.count_patients = 0

    def compute_age_from_dates(
        self, dob, deceased, dod, gender, caller, extra_date
    ):
        """ Get the person's age.
            Calculate the current age of the patient or age at time of death.
            Returns:
            If caller == 'age': str in Y-M-D,
                caller == 'childbearing_age': boolean,
                caller == 'raw_age': [Y, M, D]"""
        today = datetime.today().date()
        if dob:
            start = datetime.strptime(str(dob.date()), '%Y-%m-%d')
            end = datetime.strptime(str(today), '%Y-%m-%d')
            if extra_date:
                end = datetime.strptime(str(extra_date.date()), '%Y-%m-%d')
            if deceased and dod:
                end = datetime.strptime(str(dod.date()), '%Y-%m-%d %H:%M:%S')
            rdelta = relativedelta(end, start)
            years_months_days = str(rdelta.years) + 'a ' \
                + str(rdelta.months) + 'm ' \
                + str(rdelta.days) + 'd'
        else:
            return None
        if caller == 'age':
            return years_months_days
        elif caller == 'childbearing_age':
            if (rdelta.years >= 11
               and rdelta.years <= 55 and gender == 'f'):
                return True
            else:
                return False
        elif caller == 'raw_age':
            return [rdelta.years, rdelta.months, rdelta.days]
        else:
            return None

    @api.constrains('birthdate_date')
    def _check_birthdate_date(self):
        """ It will not allow birthdates in the future. """
        now = datetime.now()
        for record in self:
            print(record)
            if not record.birthdate_date:
                continue
            birthdate = fields.Datetime.from_string(record.birthdate_date)
            if birthdate > now:
                raise ValidationError('Partners cannot be born in the future.')
            print(
                record.birthdate_date, record.deceased, record.date_death,
                record.gender, 'age'
            )
            record.age = self.compute_age_from_dates(
                record.birthdate_date, record.deceased, record.date_death,
                record.gender, 'age', False
            )

    @api.model
    def create(self, vals):
        """ It overrides create to bind appropriate entity. """
        if all((
            vals.get('type', '').startswith('thoriumcorp.'),
            not self.env.context.get('thoriumcorp_entity_no_create'),
        )):
            model = self.env[vals['type']].with_context(
                thoriumcorp_entity_no_create=True,
            )
            thoriumcorp_entity = model.create(vals)
            return thoriumcorp_entity.partner_id
        # tmp_act = self.generate_puid()
        # for values in vals:
        #     if not values.get('ref'):
        #         values['ref'] = values.get('self.country_id')[3:]
        #     else:
        #         values['ref'] = tmp_act
        #     if 'unidentified' in values and values['unidentified']:
        #         values['ref'] = 'NN-' + values.get('ref')
        return super(ResPartner, self).create(vals)

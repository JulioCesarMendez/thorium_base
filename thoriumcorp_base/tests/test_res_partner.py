#
#    Copyright (C) 2020-2030 Thorium Corp FP <help@thoriumcorp.website.
#

from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_1 = self.env.ref(
            'thoriumcorp.res_partner_patient_1'
        )
        self.patient_1 = self.env.ref(
            'thoriumcorp.thoriumcorp.patient_patient_1'
        )

    def test_get_thoriumcorp_entity(self):
        """ Test returns correct thoriumcorp entity """
        self.partner_1.type = 'thoriumcorp.patient'
        res = self.partner_1._get_thoriumcorp_entity()
        self.assertEquals(
            res.partner_id,
            self.partner_1,
        )

    def test_get_thoriumcorp_entity_no_type(self):
        """ Test returns nothing if no type """
        self.partner_1.type = None
        self.assertFalse(
            self.partner_1._get_thoriumcorp_entity(),
        )

    def test_get_thoriumcorp_entity_not_thoriumcorp(self):
        """ Test returns nothing if not thoriumcorp type """
        self.partner_1.type = 'invoice'
        self.assertFalse(
            self.partner_1._get_thoriumcorp_entity(),
        )

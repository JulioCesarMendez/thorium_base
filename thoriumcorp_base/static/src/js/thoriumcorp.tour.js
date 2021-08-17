/*
<!--                                                                       -->
<!--    Copyright (C) 2020-2030 Thorium Corp FP <help@thoriumcorp.website  -->
<!--                                                                       -->
*/

odoo.define(
    "thoriumcorp.tour", function (require) {
        "use strict";
        var core = require('web.core');
        var tour = require('web_tour.tour');
        var _t = core._t;
        tour.STEPS.THORIUMCORP = [
            tour.STEPS.MENU_MORE,
            {
                trigger: '.o_app[data-menu-xmlid="commed.commed_root"], .oe_menu_toggler[data-menu-xmlid="commed.commed_root"]',
                content: _t('Manage electronic medicals records using the <b>Thorium Corp FP</b> app.'),
                position: 'bottom',
            },
        ];
        tour.register(
            'thoriumcorp_tour', {
                url: "/web",
            },
            tour.STEPS.THORIUMCORP
        );
    }
);

# -*- coding: utf-8 -*-
##############################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##############################################################################
{
    "name":  "POS Stocks 14",
    "summary":  "Display Stocks inside POS. Allow/Deny"
                " Order based on stocks.",
    "category":  "Point Of Sale",
    "version":  "14.0",
    "sequence":  1,
    "author":  "Wobin",
    "depends":  ['point_of_sale'],
    "data": [
        'report/receipt_report.xml',
        'data/res_groups.xml',
        'views/pos_stocks_view.xml',
        'views/template.xml',
        'views/pos_view.xml',
        'views/point_of_sale_report.xml',
    ],
    "qweb":  [
        'static/src/xml/pos_stocks.xml',
        'static/src/xml/pos.xml',
    ],
    "installable":  True,
    "auto_install":  False,
}

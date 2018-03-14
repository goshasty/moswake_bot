# -*- coding: utf-8 -*-

import gettext
gettext.install('const', './lang')

INVITE_CATEGORY = _("Choose the button")

days = [_("Monday"),_("Tuesday"),_("Wednesday"),_("Thursday"),_("Friday"),
                    _("Saturday"),_("Sunday")]
times = ["15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00"]
categories = ["wakeboard", "flyboard", "winch"]

BUTTON_POWERED = _("You powered: ")
DAY_CHOSE = _("Day: ")
TIME_CHOSE = _("Time: ")
PHONE_CHOSE = _("Phone: ")
ASK_DAY = _("Choose the day of the week")
ASK_TIME = _("Choose the time")
ASK_PHONE = _("Write your phone number where stars +7**********")
ASK_DAY_AGAIN = _("""Wrong day. Please, try again
Press /cancel to abort feeling form """)
ASK_TIME_AGAIN = _("""Wrong time. Please, try again
Press /cancel to abort feeling form """)
ASK_PHONE_AGAIN = _("""Wrong phone. Please, try again
Press /cancel to abort feeling form """)
ASK_CATEGORY_AGAIN = _("Wrong button. Please, try again")

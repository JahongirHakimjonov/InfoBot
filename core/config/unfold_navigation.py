from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": _("Home page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            }
        ],
    },
    {
        "title": _("Users"),
        "seperator": True,
        "items": [
            {
                "title": _("Foydalanuvchilar"),
                "icon": "person",
                "link": reverse_lazy("admin:auth_user_changelist"),
            },
            {
                "title": _("Guruhlar"),
                "icon": "supervisor_account",
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
            {
                "title": _("Bot foydalanuvchilari"),
                "icon": "android",
                "link": reverse_lazy("admin:infobot_botuser_changelist"),
            },
        ],
    },
    {
        "title": _("Murojaatlar"),
        "seperator": True,
        "items": [
            {
                "title": _("Investorlik murojaatlari"),
                "icon": "account_balance",
                "link": reverse_lazy("admin:infobot_applicationinvestor_changelist"),
            },
            {
                "title": _("Partnyorlik murojaatlari"),
                "icon": "handshake",
                "link": reverse_lazy("admin:infobot_applicationpartner_changelist"),
            },
        ],
    },
    {
        "title": _("Ma'lumotlar"),
        "seperator": True,
        "items": [
            {
                "title": _("Kompaniya ma'lumotlari"),
                "icon": "business",
                "link": reverse_lazy("admin:infobot_companyinfo_changelist"),
            },
            {
                "title": _("Kontakt ma'lumotlar"),
                "icon": "contact_support",
                "link": reverse_lazy("admin:infobot_contact_changelist"),
            },
            {
                "title": _("FAQ"),
                "icon": "help_outline",
                "link": reverse_lazy("admin:infobot_faq_changelist"),
            },
            {
                "title": _("Invertorlar"),
                "icon": "trending_up",
                "link": reverse_lazy("admin:infobot_investor_changelist"),
            },
            {
                "title": _("Yangiliklar"),
                "icon": "article",
                "link": reverse_lazy("admin:infobot_news_changelist"),
            },
            {
                "title": _("Partnyorlar"),
                "icon": "handshake",
                "link": reverse_lazy("admin:infobot_partner_changelist"),
            },
            {
                "title": _("Servislar"),
                "icon": "build",
                "link": reverse_lazy("admin:infobot_service_changelist"),
            },
        ],
    },
]

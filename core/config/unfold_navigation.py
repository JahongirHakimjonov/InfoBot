from django.urls import reverse_lazy

PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": "Home page",
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            }
        ],
    },
    {
        "title": "Users",
        "seperator": True,
        "items": [
            {
                "title": "Foydalanuvchilar",
                "icon": "person",
                "link": reverse_lazy("admin:auth_user_changelist"),
            },
            {
                "title": "Guruhlar",
                "icon": "supervisor_account",
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
            {
                "title": "Bot foydalanuvchilari",
                "icon": "android",
                "link": reverse_lazy("admin:infobot_botuser_changelist"),
            },
        ],
    },
    {
        "title": "Murojaatlar",
        "seperator": True,
        "items": [
            {
                "title": "Investorlik murojaatlari",
                "icon": "account_balance",
                "link": reverse_lazy("admin:infobot_applicationinvestor_changelist"),
            },
            {
                "title": "Partnyorlik murojaatlari",
                "icon": "handshake",
                "link": reverse_lazy("admin:infobot_applicationpartner_changelist"),
            },
        ],
    },
    {
        "title": "Ma'lumotlar",
        "seperator": True,
        "items": [
            {
                "title": "Kompaniya ma'lumotlari",
                "icon": "business",
                "link": reverse_lazy("admin:infobot_companyinfo_changelist"),
            },
            {
                "title": "Kontakt ma'lumotlar",
                "icon": "contact_support",
                "link": reverse_lazy("admin:infobot_contact_changelist"),
            },
            {
                "title": "FAQ",
                "icon": "help_outline",
                "link": reverse_lazy("admin:infobot_faq_changelist"),
            },
            {
                "title": "Invertorlar",
                "icon": "trending_up",
                "link": reverse_lazy("admin:infobot_investor_changelist"),
            },
            {
                "title": "Yangiliklar",
                "icon": "article",
                "link": reverse_lazy("admin:infobot_news_changelist"),
            },
            {
                "title": "Partnyorlar",
                "icon": "handshake",
                "link": reverse_lazy("admin:infobot_partner_changelist"),
            },
            {
                "title": "Servislar",
                "icon": "build",
                "link": reverse_lazy("admin:infobot_service_changelist"),
            },
        ],
    },
]

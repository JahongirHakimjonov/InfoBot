from django.templatetags.static import static

from . import unfold_navigation as navigation

UNFOLD = {
    "SITE_TITLE": "Django Default",
    "SITE_HEADER": "Django Default",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("image/logo.png"),
    "SITE_LOGO": {
        "light": lambda request: static("image/logo.png"),  # light mode
        "dark": lambda request: static("image/logo.png"),  # dark mode
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/x-icon",
            "href": lambda request: static("images/favicon.ico"),
        },
    ],
    # "LOGIN": {
    #     "image": lambda request: static("image/logo.png"),
    #     "redirect_after": lambda request: reverse_lazy("admin:auth_user_changelist"),
    # },
    "SITE_SYMBOL": "code",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "COLORS": {
        "primary": {
            "50": "220 255 230",
            "100": "190 255 200",
            "200": "160 255 170",
            "300": "130 255 140",
            "400": "100 255 110",
            "500": "70 255 80",
            "600": "50 225 70",
            "700": "40 195 60",
            "800": "30 165 50",
            "900": "20 135 40",
            "950": "10 105 30",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "uz": "🇺🇿",
                "ru": "🇷🇺",
                "en": "🇺🇸",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": navigation.PAGES,
    },
}

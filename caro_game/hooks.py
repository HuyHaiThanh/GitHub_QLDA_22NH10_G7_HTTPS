app_name = "caro_game"
app_title = "Web_caro"
app_publisher = "My_team"
app_description = "Trò chơi caro trực tuyến"
app_email = "npthanh60@gmail.com"
app_license = "agpl-3.0"

# Apps
# ------------------

# required_apps = ["frappe"]

# Desk Sections
desk_sections = [
    {
        "label": "Caro Game",
        "icon": "game-controller",
        "index": 20,
    }
]

# Desk Icons
desk_icons = [
    {
        "module_name": "Game",
        "label": "Game",
        "icon": "octicon octicon-checklist",
        "link": "game",
        "type": "module",
        "section": "Caro Game",
        "idx": 1
    },
    {
        "module_name": "Game_Core",
        "label": "Game Core",
        "icon": "octicon octicon-gear",
        "link": "game_core",
        "type": "module",
        "section": "Caro Game",
        "idx": 2
    },
    {
        "module_name": "Authentication",
        "label": "Authentication",
        "icon": "octicon octicon-key",
        "link": "authentication",
        "type": "module",
        "section": "Caro Game",
        "idx": 3
    },
    {
        "module_name": "Player",
        "label": "Player",
        "icon": "octicon octicon-person",
        "link": "player",
        "type": "module",
        "section": "Caro Game",
        "idx": 4
    },
    {
        "module_name": "Analytics",
        "label": "Analytics",
        "icon": "octicon octicon-graph",
        "link": "analytics",
        "type": "module",
        "section": "Caro Game",
        "idx": 5
    }
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/caro_game/css/caro_game.css"
app_include_js = "/assets/caro_game/js/caro_game.js"

# include js, css files in header of web template
# web_include_css = "/assets/caro_game/css/caro_game.css"
# web_include_js = "/assets/caro_game/js/caro_game.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "caro_game/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "caro_game/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "caro-home"  # Comment lại để không ghi đè trang mặc định của Frappe

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "caro_game.utils.jinja_methods",
# 	"filters": "caro_game.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "caro_game.install.before_install"
after_install = "caro_game.setup.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "caro_game.uninstall.before_uninstall"
# after_uninstall = "caro_game.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps

# before_app_install = "caro_game.utils.before_app_install"
# after_app_install = "caro_game.utils.after_app_install"

# Integration Cleanup
# -------------------

# before_app_uninstall = "caro_game.utils.before_app_uninstall"
# after_app_uninstall = "caro_game.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "caro_game.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"caro_game.tasks.all"
# 	],
# 	"daily": [
# 		"caro_game.tasks.daily"
# 	],
# 	"hourly": [
# 		"caro_game.tasks.hourly"
# 	],
# 	"weekly": [
# 		"caro_game.tasks.weekly"
# 	],
# 	"monthly": [
# 		"caro_game.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "caro_game.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "caro_game.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "caro_game.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["caro_game.utils.before_request"]
# after_request = ["caro_game.utils.after_request"]

# Job Events
# ----------
# before_job = ["caro_game.utils.before_job"]
# after_job = ["caro_game.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"caro_game.auth.validate"
# ]

# Default is 1
website_route_rules = [
	{"from_route": "/game/<path:app_path>", "to_route": "game"},
	{"from_route": "/authentication/<path:app_path>", "to_route": "authentication"},
	{"from_route": "/game-core/<path:app_path>", "to_route": "game_core"},
	{"from_route": "/player/<path:app_path>", "to_route": "player"},
	{"from_route": "/analytics/<path:app_path>", "to_route": "analytics"},
]

# Thêm cấu hình website cho các trang web
# website_redirects = [
#     {"source": "/", "target": "/home"}
# ]

# Workspaces
# ----------------
required_apps = ["frappe"]

# Đăng ký các workspaces
fixtures = [
    {"dt": "Workspace", "filters": [["module", "in", ["Game", "Game_Core", "Authentication", "Player", "Analytics"]]]}
]

# Đăng ký các Module Defs
modules = ["Game", "Game_Core", "Authentication", "Player", "Analytics", "UI", "AI"]


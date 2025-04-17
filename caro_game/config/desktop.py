# -*- coding: utf-8 -*-
from frappe import _

def get_data():
	return [
		{
			"module_name": "Caro Game",
			"color": "blue",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Caro Game")
		},
		{
			"module_name": "Game",
			"color": "grey",
			"icon": "octicon octicon-checklist",
			"type": "module",
			"label": _("Game")
		},
		{
			"module_name": "Game_Core",
			"color": "yellow",
			"icon": "octicon octicon-gear",
			"type": "module",
			"label": _("Game Core")
		},
		{
			"module_name": "Player",
			"color": "green",
			"icon": "octicon octicon-person",
			"type": "module",
			"label": _("Player")
		},
		{
			"module_name": "Analytics",
			"color": "purple",
			"icon": "octicon octicon-graph",
			"type": "module",
			"label": _("Analytics")
		}
	]
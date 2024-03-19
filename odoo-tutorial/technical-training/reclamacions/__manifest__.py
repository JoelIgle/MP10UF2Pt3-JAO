{
"name": "Reclamacions", # The name that will appear in the App list
"version": "16.0.0", # Version
"application": True, # This line says the module is an App, and not a module
"depends": ["base", "sale"], # dependencies
"data": [
     'security/ir.model.access.csv',
     'views/reclamacio_views.xml',
     'views/reclamacio_menus.xml'
],
"installable": True,
'license': 'LGPL-3',
}
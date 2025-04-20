import frappe

no_cache = True

def get_context(context):
    context.title = "Hello World"
    context.message = "Hello from Frappe!"
    return context
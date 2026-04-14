"""
tracker/routes/dashboard/__init__.py
-----------------------------------
This package groups all dashboard-related route modules.
"""

# Import dashboard route modules so their routes are registered
from . import dashboard_page
from . import add_expense
from . import delete_expense
from . import delete_selected_expenses
from . import update_expense
from . import set_budget
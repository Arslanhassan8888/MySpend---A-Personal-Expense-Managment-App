"""
tracker/routes/dashboard/__init__.py

This package contains dashboard route modules.
"""

# Import dashboard route modules so Flask can register them.
from . import dashboard_page
from . import add_expense
from . import delete_expense
from . import delete_selected_expenses
from . import update_expense
from . import set_budget

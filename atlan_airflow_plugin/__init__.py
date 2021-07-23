from airflow.plugins_manager import AirflowPlugin
import sys

from .hooks.atlan_hook import AtlanHook
from .operators.bm_operator import AtlanBmOperator

plugin_name = "atlan"


class AtlanPlugin(AirflowPlugin):
    name = plugin_name
    operators = [AtlanBmOperator]
    hooks = [AtlanHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []

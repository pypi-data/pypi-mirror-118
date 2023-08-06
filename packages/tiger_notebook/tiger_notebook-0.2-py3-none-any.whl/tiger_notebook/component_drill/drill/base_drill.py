# -*- coding:utf-8 -*-
from tiger_notebook.component_drill.util.log_util import get_logger

logger = get_logger("__name__")


class BaseDrill(object):

    code_name = None
    engine_type = None

    def get_main_file_path(self):
        return "main.py"

    def get(self, node_instance_id=None, local_dir=None):
        logger.info('get yet not implement')

    def update(self, node_instance_id=None, local_dir=None):
        logger.info('update yet not implement')

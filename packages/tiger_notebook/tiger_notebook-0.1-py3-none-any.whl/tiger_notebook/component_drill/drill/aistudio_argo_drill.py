# -*- coding:utf-8 -*-
from tiger_notebook.component_drill.drill.base_drill import BaseDrill
from tiger_notebook.component_drill.util.log_util import get_logger

logger = get_logger("__name__")


class AistudioArgoDrill(BaseDrill):
    code_name = 'aistudio_algo'
    engine_type = 1

    def get_main_file_path(self):
        return "main.py"

    def get(self, node_instance_id=None, local_dir=None):
        logger.info(node_instance_id)
        logger.info(local_dir)
        logger.info('AistudioArgoDrill get ~')

    def update(self, node_instance_id=None, local_dir=None):
        logger.info(node_instance_id)
        logger.info(local_dir)
        logger.info('AistudioArgoDrill update ~')

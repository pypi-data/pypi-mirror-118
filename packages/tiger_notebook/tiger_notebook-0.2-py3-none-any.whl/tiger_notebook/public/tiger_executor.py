# -*- coding:utf-8 -*-
from nbconvert.preprocessors.execute import ExecutePreprocessor
from nbconvert.exporters.exporter import Exporter
from traitlets import List


class TigerPreprocessor(ExecutePreprocessor):

    def preprocess(self, nb, resources=None, km=None):
        print(nb)
        print(resources)
        print(km)
        super(TigerPreprocessor, self).preprocess(nb, resources, km)

    def preprocess_cell(self, cell, resources, index):
        super(TigerPreprocessor, self).preprocess_cell(cell, resources, index)


print("Attach tiger_executor.TigerPreprocessor")
_preprocess = Exporter.default_preprocessors.default_args[0] + ['tiger_executor.TigerPreprocessor'] # noqa E501
Exporter.default_preprocessors = List(list(_preprocess)).tag(config=True) # noqa E501

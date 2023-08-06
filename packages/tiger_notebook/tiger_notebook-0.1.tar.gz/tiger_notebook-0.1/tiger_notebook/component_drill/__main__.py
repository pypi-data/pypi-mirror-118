# -*- coding:utf-8 -*-
from tiger_notebook.component_drill.drill.base_drill import BaseDrill
from tiger_notebook.component_drill import drill
import inspect
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-a', help='get/update', default='get', required=True)
parser.add_argument('-c', help='code_name')
parser.add_argument('-n', help='node_instance_id', required=True)
parser.add_argument('-d', help='local_dir', required=True)
parser.add_argument('-o', help='output')
args = parser.parse_args()


def get_engine_type(node_instance_id):
    return node_instance_id


def main():
    print(args.a)
    print(args.c)
    print(args.n)
    print(args.d)
    print(args.o)
    code_name = args.c
    node_instance_id = args.n
    local_dir = args.d
    # 获取drill
    drill_ = BaseDrill()

    code_names = {
        obj.code_name: obj for name, obj in inspect.getmembers(drill) if inspect.isclass(obj) and obj.code_name
    }
    engine_types = {
        obj.engine_type: obj for name, obj in inspect.getmembers(drill) if inspect.isclass(obj) and obj.engine_type
    }
    if code_name and code_name in code_names:
        drill_ = code_names.get(code_name)()
    else:
        engine_type = get_engine_type(node_instance_id=node_instance_id)
        print('haha %s' % engine_type)
        if engine_type and int(engine_type) in engine_types:
            print(engine_types.get(int(engine_type))())
            drill_ = engine_types.get(int(engine_type))()
    print(code_names)
    print(engine_types)

    getattr(drill_, args.a)(node_instance_id=node_instance_id, local_dir=local_dir)


if __name__ == "__main__":
    main()

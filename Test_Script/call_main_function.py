import traceback
import Lib.main_function as mf
from Test_Script import common_function as comfun

log = comfun.logger()


def execute_main_function(config_file='main_function.yml'):
    file = './Test_Data/1920x1200/config_file/' + config_file
    with open(file, 'r') as f:
        yml_obj = mf.ordered_yaml_load(file)
        for key, value in yml_obj.items():
            if value == 'Y':
                try:
                    eval(key)
                    # yml_obj[key] = "N"
                    # with open(file, 'w') as f:
                    #     mf.ordered_yaml_dump(yml_obj, f, default_flow_style=False)
                except Exception:
                    error = traceback.format_exc()
                    log.info(error)
            else:
                pass

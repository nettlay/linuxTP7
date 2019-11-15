import yaml


def get_config(element):
    path = r'./Test_Data/config.yml'
    configuration = yaml.safe_load(open(path))
    return configuration[element]

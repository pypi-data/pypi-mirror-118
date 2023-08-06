import yaml


def open_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            raise error

    return config
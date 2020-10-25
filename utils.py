import yaml


class ConfigParser:
    @staticmethod
    def parse(path=None):
        with open(path or "config.yaml", 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except Exception as err:
                print(err)

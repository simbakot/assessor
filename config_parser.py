import yaml


class Config(object):
    def __init__(self, filename):
        self.filename = filename
        self._config = self._parse()

        self.database = self._load_property('database', default=None)

    def _parse(self):
        with open(self.filename, 'r') as f:
            return yaml.safe_load(f)

    def _load_property(self, key, default=None):
        assert hasattr(self, '_config') and self._config is not None
        return self._config[key] if key in self._config else default

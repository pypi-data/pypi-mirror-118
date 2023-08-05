import re
from .logger import Logger
from .providers import StoreProvider, Providers
from .stages import Stages
from .constants import *
from .exceptions import *


REGEX_PATTERN  = r"^[a-zA-Z]([.a-zA-Z0-9_-]*[a-zA-Z0-9])?$"

class ParameterProvider(StoreProvider):
    def list(self, config, uninherited=False, filter=None):
        raise NotImplementedError()
    def add(self, config, key, value):
        raise NotImplementedError()
    def get(self, config, key, revision=None):
        raise NotImplementedError()
    def history(self, config, key):
        raise NotImplementedError()
    def delete(self, config, key):
        raise NotImplementedError()


class ParameterService():

    def validate_key(self, key):
        Logger.info(f"Validating parameter key '{key}'...")
        if not key:
            raise DSOException(MESSAGES['KeyNull'])
        if key == 'dso' or key.startswith('dso.'):
            raise DSOException(MESSAGES['DSOReserverdKey'].format(key))
        if not re.match(REGEX_PATTERN, key):
            raise DSOException(MESSAGES['InvalidKeyPattern'].format(key, REGEX_PATTERN))
        if '..' in key:
            raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '..'))
            
    def list(self, config, uninherited=False, filter=None):
        self.config = config
        project = config.project
        application = config.application
        stage = Stages.normalize(config.stage)
        provider = Providers.ParameterProvider()
        Logger.info(f"Start listing parameters: project={project}, application={application}, stage={Stages.shorten(stage)}")
        return provider.list(config, uninherited, filter)

    def add(self, config, key, value):
        self.config = config
        project = config.project
        application = config.application
        stage = Stages.normalize(config.stage)
        self.validate_key(key)
        Logger.info(f"Start adding parameter '{key}': project={project}, application={application}, stage={Stages.shorten(stage)}")
        provider = Providers.ParameterProvider()
        return provider.add(config, key, value)

    def get(self, config, key, revision=None):
        # self.validate_key(key)
        self.config = config
        project = config.project
        application = config.application
        stage = Stages.normalize(config.stage)
        provider = Providers.ParameterProvider()
        Logger.info(f"Start getting the details of parameter '{key}': project={project}, application={application}, stage={Stages.shorten(stage)}")
        return provider.get(config, key, revision)

    def history(self, config, key):
        # self.validate_key(key)
        self.config = config
        project = config.project
        application = config.application
        stage = Stages.normalize(config.stage)
        provider = Providers.ParameterProvider()
        Logger.info(f"Start getting the history of parameter '{key}': project={project}, application={application}, stage={Stages.shorten(stage)}")
        return provider.history(config, key)

    def delete(self, config, key):
        # self.validate_key(key)
        self.config = config
        project = config.project
        application = config.application
        stage = Stages.normalize(config.stage)
        provider = Providers.ParameterProvider()
        Logger.info(f"Start deleting parameter '{key}': project={project}, application={application}, stage={Stages.shorten(stage)}")
        return provider.delete(config, key)

Parameters = ParameterService()
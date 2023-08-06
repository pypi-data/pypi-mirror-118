"""
    env_configurator helps you to get Environment Variables easily
    =====================
"""
import os
from EnvConfigurator.exceptions import EnvVarValueNotValid, EnvVarNotFound


class EnvVar:
    """
        Some Description Here
        =====================
        And what more ?
    """

    supported_env_types = [str, int, float, list]

    def __init__(self, name, var_type, optional=False, default=None, choices=None, custom_msg=None, separator=" "):
        """
        args:
            name: Name of Environment Variable
                type: str
            var_type: Type of Environment Variable
                type: str/bool/int/float/list
            choices: Env Var choices to select
            optional: If Environment Variable can be skipped
        """
        self.name = name
        self.var_type = var_type
        self.optional = optional
        self.default = default
        self.choices = [] if choices is None else choices
        self.custom_msg = custom_msg
        self.list_separator = separator

        self.__validate_config()

    def __validate_config(self):
        if type(self.name) != str:
            exception_msg = f"__class__ is not configured properly. " \
                            f"'name' should be of 'str' type"
            raise Exception(exception_msg)

        # if self.var_type != type:
        #     exception_msg = f"__class__ is not configured properly. " \
        #                     f"'var_type' belong to 'type' class and "
        #     raise Exception(exception_msg)

    def __handle_bool(self, env_value):
        if env_value.upper() in ["TRUE", "1"]:
            return True
        elif env_value.upper() in ["FALSE", "0"]:
            return False
        else:
            exception_msg = f"{self.name} value is not valid. " \
                            f"Expected True/1 or False/0, got {env_value}"
            raise EnvVarValueNotValid(exception_msg)


    def validate(self, env_value):

            if not env_value:
                if self.optional:
                    return self.default
                else:
                    exception_msg = f"{self.name} value is not valid. " \
                                    f"Expected {'|'.join(self.choices)}, got {env_value}"
                    raise EnvVarValueNotValid(exception_msg)

            if type(env_value) != self.var_type:
                try:
                    if self.var_type is int:
                        env_value = int(env_value)
                    elif self.var_type is float:
                        env_value = int(env_value)
                    elif self.var_type is list:
                        env_value = env_value.split(self.list_separator)
                    elif self.var_type is bool:
                        env_value = self.__handle_bool(env_value)

                except ValueError:
                    exception_msg = f"{self.name} type is not valid. " \
                                    f"Expected {str(self.var_type)}, got {str(type(env_value))}"
                    raise EnvVarValueNotValid(exception_msg)

            if self.choices and env_value not in self.choices:
                exception_msg = f"{self.name} value is not valid. " \
                                f"Expected {'|'.join(self.choices)}, got {env_value}"
                raise EnvVarValueNotValid(exception_msg)

            return env_value


class ProcessedEnv:
    """
        Some Description Here
        =====================
        And what more ?
    """

    @classmethod
    def add_new_env(cls, env_name, env_value):
        setattr(cls, env_name, env_value)


class EnvParser:
    """
        Some Description Here
        =====================
        And what more ?
    """

    config_type = EnvVar

    def __init__(self, env_vars, logger=None):
        """
        args:
            config:
                type: list, list object type: config.EnvVar
        """
        self.env_vars = env_vars
        self.__validate_config()

        self.__logger = logger
        self.__env_os = os.environ.copy()

        self.all = self.__parse_all_env()

    def __validate_config(self):
        if type(self.env_vars) != list:
            exception_msg = f"__class__ is not configured properly. " \
                            f"'config' is required as list of config.EnvVar"
            raise Exception(exception_msg)

    def __parse_single_env(self, env_var):
        """
        args:
            env_var:
                type: EnvVar
        """
        env_value = self.__env_os.get(env_var.name)
        return env_var.validate(env_value)

    def __parse_all_env(self):
        for env_var in self.env_vars:
            env_value = self.__parse_single_env(env_var)
            ProcessedEnv.add_new_env(env_var.name, env_value)

        return ProcessedEnv

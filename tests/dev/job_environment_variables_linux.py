#! python3  # noqa: E265
import logging

from sys import platform as opersys

if opersys == 'linux':
    from dev_manage_persistent_env_var_linux import (
        delete_environment_variable,
        update_environment_variable,
        set_environment_variable,
    )
elif opersys == 'win32':
    from qgis_deployment_toolbelt.utils.win32utils import (
        delete_environment_variable,
        refresh_environment,
        set_environment_variable,
    )
else:
    logger.debug(
        "Unsupported operating system."
    )
    exit()


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s||%(levelname)s||%(module)s||%(lineno)d||%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

options: [dict] = [
    {
        'name': 'TEST_PERSISTENT_ENVIRONMENT_VARIABLE',
        'action': 'add',
        'scope': 'user',
        'value': 'True',
        'value_type': 'bool',
    }
]

def prepare_value(value: str, value_type: str = None) -> str:
    """Prepare value to be used in the environment variable.

    It performs some checks or operations depending on value type: user and
        variable expansion, check if URL is valid, etc.

    Args:
        value (str): value to prepare.
        value_type (str, optional): type of input value. Defaults to "str".

    Returns:
        str: prepared value.
    """

    if value_type == "url":
        if check_str_is_url(input_str=value, raise_error=False):
            logger.info(
                f"{value} is a valid URL. Using it as environment variable value."
            )
        else:
            logger.warning(
                f"{value} seems to be an invalid URL. " "It will be applied anyway."
            )

        return value.strip()
    elif value_type in ("bool", "str"):
        return str(value).strip()
    elif value_type == "path":
        # test if value is a path
        if check_var_can_be_path(input_var=value, raise_error=False):
            value_as_path = Path(expanduser(expandvars(value)))
            if not check_path_exists(input_path=value_as_path, raise_error=False):
                logger.warning(
                    f"{value} seems to be a valid path but does not exist (yet)."
                )
            return str(Path(value_as_path).resolve())
        else:
            logger.debug(
                f"Value {value} is not a valid path. The raw string will be used."
            )

    return str(value).strip()

if opersys == "win32":
    logger.debug(
        f"OS : {opersys}"
    )
    '''
    for env_var in self.options:
        if env_var.get("action") == "add":
            try:
                set_environment_variable(
                    envvar_name=env_var.get("name"),
                    envvar_value=self.prepare_value(
                        value=env_var.get("value"),
                        value_type=env_var.get("value_type"),
                    ),
                    scope=env_var.get("scope"),
                )
            except NameError:
                logger.debug(
                    f"Variable name '{env_var.get('name')}' is not defined"
                )
        elif env_var.get("action") == "remove":
            try:
                delete_environment_variable(
                    envvar_name=env_var.get("name"),
                    scope=env_var.get("scope"),
                )
            except NameError:
                logger.debug(
                    f"Variable name '{env_var.get('name')}' is not defined"
                )
    # force Windows to refresh the environment
    refresh_environment()
    '''

# TODO: for linux, edit ~/.profile or add a .env file and source it from ~./profile
elif opersys == "linux":
    logger.debug(
         f"OS : {opersys}"
    )
    for env_var in options:
        print(f'ACTION {env_var.get("action")}', f'NAME {env_var.get("name")}', f'VALUE {env_var.get("value")}')
        if env_var.get("action") == "add":
            try:
                set_environment_variable(
                    env_key=env_var.get("name"),
                    env_value=prepare_value(
                        value=env_var.get("value"),
                        value_type=env_var.get("value_type"),
                    ),
                    scope=env_var.get("scope")
                )
            except NameError:
                logger.debug(
                    f"Variable name '{env_var.get('name')}' is not defined"
                )
        elif env_var.get("action") == "remove":
            try:
                delete_environment_variable(
                    envvar_name=env_var.get("name"),
                    scope=env_var.get("scope")
                )
            except NameError:
                logger.debug(
                    f"Variable name '{env_var.get('name')}' is not defined"
                )
        elif env_var.get("action") == "update":
            try:
                update_environment_variable(
                    envvar_name=env_var.get("name"),
                    envvar_value=self.prepare_value(
                        value=env_var.get("value"),
                        value_type=env_var.get("value_type"),
                    ),
                    scope=env_var.get("scope")
                )
            except NameError:
                logger.debug(
                    f"Variable name '{env_var.get('name')}' is not defined"
                )
    # force Linux to refresh the environment ?

else:
    logger.debug(
        f"Setting persistent environment variables is not supported on {opersys}"
    )




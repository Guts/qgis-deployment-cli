import os
from configparser import BasicInterpolation, ConfigParser
from os import environ
from pathlib import Path

environ["QDT_TEST_ENV_VARIABLE"] = "fake value"


class EnvInterpolation(BasicInterpolation):
    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        print(type(parser), type(section), type(option), type(value), type(defaults))
        return os.path.expandvars(value)


qgis3ini_filepath = Path(__file__).parent.parent.joinpath(
    "fixtures/qgis_ini/test_ini_interpolated.ini"
)
assert qgis3ini_filepath.exists(), FileExistsError(qgis3ini_filepath)
config = ConfigParser(
    strict=False,
    interpolation=EnvInterpolation(),
    defaults={"no_existing_key": "default_value"},
)
config.optionxform = str
config.read(qgis3ini_filepath, encoding="UTF8")

for section in config.sections():
    print(f"Section: {section}")
    for key in config[section]:
        print(f"  {key} = {config[section][key]}")
print(config.get(section="test", option="qdt_working_directory"))

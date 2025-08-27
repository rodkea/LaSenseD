from typing import TypedDict
import json

class ConfigType(TypedDict):

  Brightness : float
  Contrast : float
  ISO : float
  Sharpness : float


USER_CONFIG_PATH = "Config/user.config"
DEFAULT_CONFIG_PATH = "Config/default.config"


def read_config(file_path : str) -> ConfigType:
    """Read configuration settings from a file and returns them as a dictionary.

        Args:
    file_path (str): The path to the configuration file.

    Returns:
        ConfigType: A dictionary containing the configuration settings read from the file.
    """
    try:
        with open(file_path, 'r') as file:
            config_data = json.load(file)
        return ConfigType(
            Brightness = config_data["Brightness"],
            Contrast = config_data["Contrast"],
            ISO = config_data["ISO"],
            Sharpness = config_data["Sharpness"]        
        )  
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error reading configuration file: {e}")
        raise
    
def write_config(file_path : str, config : ConfigType):
    """Write the config settings to a file.
    
    Args:
      file_path (str): The path to the configuration file.
      config (ConfigType): The configuration dictionary to save in the file as json.
    """
    try:
      with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)
    except Exception as e:
      print(f"Error writing config file {e}")
      raise    
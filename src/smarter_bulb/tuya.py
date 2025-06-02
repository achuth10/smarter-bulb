"""
Tuya API client
"""

from tuya_connector import (
    TuyaOpenAPI,
)
from config import TUYA_CONFIG


def get_tuya_client():
    """
    Get Tuya client
    """
    openapi = TuyaOpenAPI(
        endpoint=TUYA_CONFIG["API_ENDPOINT"],
        access_id=TUYA_CONFIG["CLIENT_ID"],
        access_secret=TUYA_CONFIG["CLIENT_SECRET"],
    )
    openapi.connect()
    return openapi


def control_bulb(control: dict):
    """
    Control a Wipro/Tuya smart bulb using a structured settings dictionary.

    Args:
        control (dict): Dictionary of settings with optional keys:
            - power (bool): Turn light ON/OFF.
            - brightness (int): Brightness level (10–1000).
            - color_temp (int): White temperature (0–1000).
            - color (dict): {'h': int, 's': int, 'v': int} for HSV color.
            - mode (str): One of ['white', 'colour', 'scene', 'music'].
            - scene (dict): {'scene_num': int, 'scene_units': [dict, ...]}.
            - countdown (int): Seconds until auto-off (0–86400).
    """

    # Build the command payload
    commands = []

    if "power" in control:
        commands.append({"code": "switch_led", "value": control["power"]})

    if "mode" in control:
        commands.append({"code": "work_mode", "value": control["mode"]})

    if "brightness" in control:
        commands.append({"code": "bright_value_v2", "value": control["brightness"]})

    if "color_temp" in control:
        commands.append({"code": "temp_value_v2", "value": control["color_temp"]})

    if "color" in control:
        commands.append(
            {
                "code": "colour_data_v2",
                "value": {
                    "h": control["color"]["h"],
                    "s": control["color"]["s"],
                    "v": control["color"]["v"],
                },
            }
        )

    if "scene" in control and control["scene"] is not None:
        scene_data = {"scene_num": control["scene"]["scene_num"]}
        if "scene_units" in control["scene"]:
            scene_data["scene_units"] = control["scene"]["scene_units"]
        commands.append({"code": "scene_data_v2", "value": scene_data})

    if "countdown" in control:
        commands.append({"code": "countdown_1", "value": control["countdown"]})
    payload = {"commands": commands}

    tuya_client = get_tuya_client()

    response = tuya_client.post(
        f"/v1.0/devices/{TUYA_CONFIG['DEVICE_ID']}/commands",
        body=payload,
    )
    return response


control_bulb_function_schema = {
    "name": "control_bulb",
    "type": "function",
    "description": "Control a Wipro/Tuya smart bulb with settings such as power, brightness, color, temperature, mode, scenes, or a countdown timer.",
    "parameters": {
        "type": "object",
        "properties": {
            "control": {
                "type": "object",
                "description": "A dictionary of settings to apply to the smart bulb.",
                "properties": {
                    "power": {
                        "type": "boolean",
                        "description": "Turn the light ON or OFF (does not power off the device, only the LED).",
                    },
                    "brightness": {
                        "type": "integer",
                        "minimum": 10,
                        "maximum": 1000,
                        "description": "Set brightness level (10–1000).",
                    },
                    "color_temp": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 1000,
                        "description": "Set white color temperature: 0 = warmest, 1000 = coolest.",
                    },
                    "color": {
                        "type": "object",
                        "description": "Set color using HSV format. Must set mode to 'colour' to apply.",
                        "properties": {
                            "h": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 360,
                                "description": "Hue (0–360 degrees).",
                            },
                            "s": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 1000,
                                "description": "Saturation (0–1000).",
                            },
                            "v": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 1000,
                                "description": "Brightness value (0–1000).",
                            },
                        },
                        "required": ["h", "s", "v"],
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["white", "colour", "scene", "music"],
                        "description": "Select operating mode: 'white' for temperature control, 'colour' for HSV color, 'scene' for animated scenes, or 'music' to sync with sound.",
                    },
                    "scene": {
                        "type": "object",
                        "description": "Apply a preset or custom scene animation (use with mode 'scene').",
                        "properties": {
                            "scene_num": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 8,
                                "description": "Built-in scene number (1–8).",
                            },
                            "scene_units": {
                                "type": "array",
                                "description": "Optional array of custom color steps for the scene.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "unit_change_mode": {
                                            "type": "string",
                                            "enum": ["static", "jump", "gradient"],
                                            "description": "Transition style between colors.",
                                        },
                                        "unit_switch_duration": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 100,
                                            "description": "Time to hold each color before transition (in seconds).",
                                        },
                                        "unit_gradient_duration": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 100,
                                            "description": "Time to fade between colors (in seconds).",
                                        },
                                        "bright": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 1000,
                                            "description": "Brightness for this step.",
                                        },
                                        "temperature": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 1000,
                                            "description": "White color temperature for this step (optional).",
                                        },
                                        "h": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 360,
                                            "description": "Hue for this step.",
                                        },
                                        "s": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 1000,
                                            "description": "Saturation for this step.",
                                        },
                                        "v": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 1000,
                                            "description": "Brightness value for this step.",
                                        },
                                    },
                                    "required": [
                                        "unit_change_mode",
                                        "unit_switch_duration",
                                        "unit_gradient_duration",
                                        "bright",
                                        "h",
                                        "s",
                                        "v",
                                    ],
                                },
                            },
                        },
                        "required": ["scene_num"],
                    },
                    "countdown": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 86400,
                        "description": "Set a timer (in seconds) to automatically turn the light off. 0 = no timer.",
                    },
                },
            }
        },
        "required": ["control"],
    },
}

# Example command
# commands = {
#     "power": True,
#     "color": {"h": 0, "s": 1000, "v": 1000},
#     "mode": "colour",
# }
# control_bulb(commands)

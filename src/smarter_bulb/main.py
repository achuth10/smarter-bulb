"""
Control a Wipro/Tuya smart bulb with settings such as power, brightness, color, temperature, mode, scenes, or a countdown timer.
"""

import argparse
import json

from openai_client import openai_client
from tuya import control_bulb, control_bulb_function_schema

tool_set = [control_bulb_function_schema]


def main():
    """
    Main function to control the bulb using natural language
    """
    parser = argparse.ArgumentParser(
        description="Control smart bulb using natural language"
    )
    parser.add_argument(
        "command", type=str, help="Natural language command to control the bulb"
    )
    args = parser.parse_args()

    system_message = {
        "role": "system",
        "content": (
            "You are a smart home assistant. Interpret short user inputs like 'blue', 'off', 'bright' "
            "and convert them to full parameters to control the smart bulb. "
            "If user input is 'off' or 'turn off', set power to false. "
            "If color name is given, convert it to approximate HSV values. "
            "If brightness is not specified, use a default brightness of 500. "
            "If a colour is given. always set power to true"
            "Always return function calls only with valid JSON arguments."
        ),
    }
    input_messages = [
        {
            "role": "user",
            "content": args.command,
        }
    ]

    response = openai_client.responses.create(
        model="gpt-4o-mini",
        input=[system_message, *input_messages],
        tools=tool_set,
    )

    response_json = response.output[0].to_dict()
    arguments = json.loads(response_json["arguments"])

    control_bulb(arguments["control"])


if __name__ == "__main__":
    main()

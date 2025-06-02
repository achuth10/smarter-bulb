# smarter-bulb

> Have you ever had the first world problem of your smartphone and Alexa being just too far away, and flipping a light switch is so 20th century? Well, this is for you.

## What is this?

**smarter-bulb** is a Python command-line tool that lets you type things like "blue," "off," or "make it look like a rave in here" and, through the magic of large language models (LLMs), your smart bulb will (probably) do what you want. It's the future, and the future is bright—unless you say "off," in which case it's not.

## How Does It Work?

Let's break it down:

1. **You Type a Command**  
   Not a real command, mind you. Just whatever pops into your head. "Red." "Turn off." "I want to feel like I'm in a dentist's office." The script doesn't judge.

2. **The LLM Interprets Your Nonsense**  
   The script sends your input to an LLM (OpenAI's GPT-4o-mini, because we're not made of money), along with a system prompt that basically says, "Hey, pretend you're a smart home assistant. If the user says 'off,' turn the bulb off. If they say a color, turn it on and make it that color. If they don't specify brightness, just pick something reasonable. And for the love of all that is holy, only return valid JSON."

3. **The Bulb Obeys**  
   The script then takes the LLM's output, decodes the JSON, and sends the appropriate command to your Wipro/Tuya bulb. The bulb, which has no idea it's part of this absurd chain of events, dutifully changes color, brightness, or power state.

## Why Would Anyone Do This?

- **Because You Can:** Why settle for a light switch when you can have a Python script, an LLM, and a Wi-Fi-enabled bulb all working together to do the same thing, but slower and with more points of failure?

## Requirements

- Python 3.8+
- A Wipro/Tuya smart bulb
- OpenAI API key (the LLM isn't powered by good vibes)
- The `openai_client` and `tuya` Python modules (see below)
- **Your Tuya Device ID**
- **Tuya Cloud Project**

## Installation

### Setting Up a Cloud Project in Tuya

Before you can control your bulb, you need to set up a cloud project in Tuya. Here's how:

1. **Create a Tuya Developer Account:**  
   Go to the [Tuya IoT Platform](https://iot.tuya.com/) and sign up for a developer account.

2. **Create a Cloud Project:**

   - Navigate to the "Cloud Development" section.
   - Click "Create Cloud Project" and follow the prompts to set up your project.
   - Note down the **Client ID** and **Client Secret** provided for your project.

### Finding Your Tuya Device ID

Before you can control your bulb, you need to find its device ID. Here's how:

1. Open the Tuya Smart app on your smartphone.
2. Navigate to your bulb's settings.
3. Look for the device ID (it might be labeled as "Device ID," "ID," or something similar).
4. Copy that ID. You'll need it later.

Clone this repo, cd into it, and install dependencies:

```bash
git clone <this-repo-url>
cd smarter-bulb
pip install -r requirements.txt
```

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=sk-...
export TUYA_CLIENT_ID=your_client_id
export TUYA_CLIENT_SECRET=your_client_secret
export TUYA_DEVICE_ID=your_device_id

```

Or rename .env-sample to .env and the credentials there

## Usage

```bash
python smarter-bulb/src/smarter_bulb/main.py "blue"
```

Or try:

```bash
python smarter-bulb/src/smarter_bulb/main.py "turn off"
python smarter-bulb/src/smarter_bulb/main.py "make it bright and green"
python smarter-bulb/src/smarter_bulb/main.py "I want a cozy warm light"
```

### Using with Raycast

You can also use this project with Raycast by creating a bash script that lets you run the file as a spotlight command. So you dont have to be a plebian and run the python script manually ever:

1. **Create a Bash Script:**  
   Create a file named `control_bulb.sh` with the following content:

   ```bash
    #!/bin/bash
    # Required parameters:
    # @raycast.schemaVersion 1
    # @raycast.title bulb
    # @raycast.mode silent

    # Optional parameters:
    # @raycast.icon 🤖
    # @raycast.argument1 { "type": "text", "placeholder": "switch on the bulb" }

    # Documentation:
    # @raycast.description Control the bulb in your room
    # @raycast.author Achuth

    cd path/to/repo
    source venv/bin/activate
    python main.py "$1"
   ```

   Replace `/path/to/project` with the actual path to your project. Activate a venv here if using.

2. **Make the Script Executable:**  
   Run the following command to make the script executable:

   ```bash
   chmod +x control_bulb.sh
   ```

3. **Set Up Raycast:**
   - Open Raycast and go to the "Scripts" section.
   - Add a new script and set the command to `./control_bulb.sh`.
   - Now you can use Raycast to control your bulb with natural language commands.

Now with this in place you can do this:

<iframe width="560" height="315" src="https://www.youtube.com/embed/your_video_id" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Limitations

- Requires a Wipro/Tuya bulb (not included)
- Needs an OpenAI API key (also not included)
- May occasionally hallucinate (the AI, not you—hopefully)
- If your bulb starts flashing Morse code, blame the AI

## Contributing

Pull requests welcome! If you can make the LLM less likely to hallucinate or your bulb more likely to obey, you're a hero.

## License

MIT. Because if you break your bulb, your house, or your spirit, that's on you.

# Inspector Max Project

## Overview

Inspector Max is an advanced integration project that combines the agility of Boston Dynamics' Spot robot with the cutting-edge capabilities of GPT-4 Vision and voice command technologies. Inspired by the iconic roles of Arnold Schwarzenegger, Inspector Max is designed to perform a variety of tasks using voice commands, visual data processing, and autonomous navigation. This project aims to showcase the potential of combining AI and robotics in performing complex tasks.

## Features

- **Voice Command Recognition**: Utilizes advanced voice recognition to interpret and execute commands spoken by authorized users.
- **GPT-4 Vision Integration**: Leverages the GPT-4 Vision model to analyze visual data, allowing Inspector Max to describe scenes, identify objects, and more.
- **Autonomous Navigation**: Empowers Spot to patrol areas, and interact with its surroundings.
- **Interactive Responses**: Generates human-like responses in the persona of Arnold Schwarzenegger, enhancing user interaction.
- **Task Execution**: Performs tasks such as patrolling, sitting, standing up, and expressing gratitude upon command.

## Prerequisites

Before you begin, ensure you have the following:

- Access to a Spot robot from Boston Dynamics.
- An account on Merklebot for robot interactions
- A system with Docker installed for building and running the Inspector Max container.
- An OpenAI API key for accessing GPT-4 and GPT-4 Vision capabilities.
- An ElevenLabs API key for voice synthesis.

## Setup Instructions

0. Account Creation

- Visit [Merklebot](https://app.merklebot.com) and create an account. This account will be the primary interface for all interactions with Spot.
- Once your account is set up, you will use Merklebot's web interface to launch and manage Docker containers for interacting with Spot.

1. **Clone the Repository**: Clone the Inspector Max project repository to your local machine.

    ```bash
    git clone https://github.com/CodeMetalAI/hackathon-agi-house.git
    cd hackathon-agi-house
    ```

2. **Build the Docker Image**: Navigate to the project directory and build the Docker image.

    ```bash
    docker build -t inspector-max .
    ```
3. **Run the Docker Container**: Start the container with the necessary device and environment variables.

    ```bash
    docker run --rm -it --device /dev/video0 --device /dev/snd -e SDL_AUDIODRIVER='alsa' -e AUDIODEV='hw:1,0' -e AUDIO_INPUT_DEVICE='hw:2,0' inspector-max
    ```

## Usage

- **Starting Inspector Max**: Once the Docker container is up, Inspector Max is ready to receive voice commands.
- **Voice Commands**: Speak directly to Inspector Max to perform tasks. Here are some example commands:
  - "Patrol the area": Initiates a patrol sequence.
  - "Describe this": Uses GPT-4 Vision to analyze and describe the current scene.
  - "Sit down": Commands Inspector Max to sit.
  - "Stand up": Commands Inspector Max to resume a standing position.
  - "Good boy": Expresses gratitude, to which Inspector Max responds appreciatively.

## Contribution

We welcome contributions to the Inspector Max project. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Boston Dynamics for the Spot robot platform.
- OpenAI for GPT-4 and GPT-4 Vision technologies.
- ElevenLabs for voice synthesis capabilities.

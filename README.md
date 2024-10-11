# lol-champion-skills-video-generator

This repository is used to generate videos in multiple languages, ​​presenting the abilities of all champions of the game [League of Legends](https://www.leagueoflegends.com/), by fetching the data from [leagueoflegends.com](https://www.leagueoflegends.com/).

## Getting Started

### Prerequisites

- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) 20 (with npm)
- [Python](https://www.python.org/) 3 (with pip)

### Installation

Installation guide for Windows, but should also work easily on Linux.

- Clone this repository

    ```
    git clone https://github.com/pierre-josselin/lol-champion-skills-video-generator.git
    ```

- Access the cloned repository

    ```
    cd .\lol-champion-skills-video-generator
    ```

- Create and edit the environment file

    ```
    copy .env.example .env
    ```

- Install Node.js dependencies

    ```
    npm install
    ```

- Install Python dependencies

    ```
    pip install dotenv opencv-python moviepy
    ```

- Download and install [ImageMagick](https://imagemagick.org/)

    > It could be required to check "Install legacy utilities (e.g. convert)" during the installation.

- Edit the `IMAGE_MAGICK_BINARY_PATH` variable from the environment file.

## Usage

- Fetch the champions

    ```
    node .\index.js fetch-champions en-us
    ```

- Fetch the champions media

    ```
    node .\index.js fetch-champions-media .\champions\champions.en-us.json
    ```

- Generate the champions videos

    ```
    node .\index.js generate-champions-videos .\champions\champions.en-us.json
    ```

    > It may take several hours to generate the champions videos.

- Generate the video

    ```
    python .\main.py generate-video .\champions\champions.en-us.json .\output.mp4
    ```

# lol-champion-skills-video-generator

This repository is used to generate videos in multiple languages, ​​presenting the abilities of all champions of the game [League of Legends](https://www.leagueoflegends.com/), by fetching the data from [leagueoflegends.com](https://www.leagueoflegends.com/).

[🎬 YouTube demo video](https://www.youtube.com/watch?v=F7KJz1ZVFbw)

## Getting Started

### Prerequisites

- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) 20 (with npm)
- [Python](https://www.python.org/) 3 (with pip)
- [ImageMagick](https://imagemagick.org/) (with legacy utilities)

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

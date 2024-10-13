const axios = require("axios");
const childProcess = require("child_process");
const dotenv = require("dotenv");
const fs = require("fs/promises");
const nodeHtmlParser = require("node-html-parser");
const path = require("path");
const striptags = require("striptags");
const util = require("util");
const { createWriteStream } = require("fs");
const { setTimeout } = require("timers/promises");

const execute = util.promisify(childProcess.exec);

const championsDirectoryPath = "./champions";

dotenv.config();

async function requestInterceptor(config) {
    console.log(config.url);
    await setTimeout(parseInt(process.env.REQUEST_DELAY));
    return config;
}

const leagueOfLegends = axios.create({
    baseURL: process.env.LEAGUE_OF_LEGENDS_URL
});

axios.interceptors.request.use(requestInterceptor);
leagueOfLegends.interceptors.request.use(requestInterceptor);

async function fetchMedia(url, path) {
    const response = await axios({
        url,
        method: "GET",
        responseType: "stream"
    });

    const stream = createWriteStream(path);
    response.data.pipe(stream);

    return new Promise((resolve, reject) => {
        stream.on("finish", resolve);
        stream.on("error", reject);
    });
}

async function fetchChampions(language) {
    const response = await leagueOfLegends.get(`/${language}/champions`);
    const document = nodeHtmlParser.parse(response.data);
    const element = document.getElementById("__NEXT_DATA__");
    const data = JSON.parse(element.innerText);
    const characterCardGrid = data.props.pageProps.page.blades.find((blade) => blade.type === "characterCardGrid");
    const urls = characterCardGrid.items.map((item) => item.action.payload.url);

    const champions = [];
    for (const url of urls) {
        const response = await leagueOfLegends.get(url);
        const document = nodeHtmlParser.parse(response.data);
        const element = document.getElementById("__NEXT_DATA__");
        const data = JSON.parse(element.innerText);
        const page = data.props.pageProps.page;
        const characterMasthead = page.blades.find((blade) => blade.type === "characterMasthead");
        const iconTab = page.blades.find((blade) => blade.type === "iconTab");

        champions.push({
            id: page.id.split(".")[1],
            name: characterMasthead.title,
            description: characterMasthead.description?.body ? striptags(characterMasthead.description.body) : "",
            title: characterMasthead.subtitle,
            difficulty: characterMasthead.difficulty.value,
            splash: characterMasthead.backdrop.background.url,
            roles: characterMasthead.role.roles.map((role) => role.id),
            abilities: iconTab.groups.map((group) => ({
                name: group.content.title,
                description: striptags(group.content.description.body),
                image: group.thumbnail.url,
                videos: group.content?.media?.sources?.map((source) => source.src) ?? []
            }))
        });
    }

    await fs.mkdir(championsDirectoryPath, { recursive: true });
    await fs.writeFile(`${championsDirectoryPath}/champions.${language}.json`, JSON.stringify(champions, null, 4));
}

async function fetchChampionsMedia(champions) {
    for (const [index, champion] of champions.entries()) {
        console.log(champion.name, `(${index + 1}/${champions.length})`);

        await fs.mkdir(`${championsDirectoryPath}/${champion.id}/abilities/images`, { recursive: true });
        await fs.mkdir(`${championsDirectoryPath}/${champion.id}/abilities/videos`, { recursive: true });

        const name = champion.splash.substring(champion.splash.lastIndexOf("/") + 1, champion.splash.lastIndexOf("_"));
        const image = champion.abilities[0].image.split("/").slice(0, 6).join("/") + `/champion/${name}.png`;

        try {
            await fetchMedia(image, `${championsDirectoryPath}/${champion.id}/image.png`);
        } catch (error) {
            console.error(image);
        }

        if (champion.splash) {
            try {
                await fetchMedia(champion.splash, `${championsDirectoryPath}/${champion.id}/splash${path.extname(champion.splash)}`);
            } catch (error) {
                console.error(champion.splash);
            }
        }

        for (const [index, ability] of champion.abilities.entries()) {
            if (ability.image) {
                try {
                    await fetchMedia(ability.image, `${championsDirectoryPath}/${champion.id}/abilities/images/${index}${path.extname(ability.image)}`);
                } catch (error) {
                    console.error(ability.image);
                }
            }

            if (ability.videos && ability.videos.length) {
                let success = false;
                for (const video of ability.videos) {
                    try {
                        await fetchMedia(video, `${championsDirectoryPath}/${champion.id}/abilities/videos/${index}${path.extname(video)}`);
                        success = true;
                        break;
                    } catch (error) {
                    }
                }
                if (!success) {
                    ability.videos.map((video) => console.error(video));
                }
            }
        }
    }
}

async function generateChampionsVideos(champions, championsFilePath, resume) {
    if (!resume) {
        for (const champion of champions) {
            const videoPath = path.join(championsDirectoryPath, champion.id, "video.mp4");
            try {
                await fs.unlink(videoPath);
            } catch (error) {
            }
        }
    }

    for (const [index, champion] of champions.entries()) {
        console.log(champion.name, `(${index + 1}/${champions.length})`)

        if (resume) {
            try {
                await fs.access(path.join(championsDirectoryPath, champion.id, "video.mp4"));
                continue;
            } catch (error) {
            }
        }

        await execute(`python ${path.join(".", "main.py")} generate-champion-video ${championsFilePath} ${champion.id}`)
    }
}

async function main() {
    switch (process.argv[2]) {
        case "fetch-champions": {
            await fetchChampions(process.argv[3]);
            break;
        }
        case "fetch-champions-media": {
            const data = await fs.readFile(process.argv[3]);
            const champions = JSON.parse(data);
            await fetchChampionsMedia(champions);
            break;
        }
        case "generate-champions-videos": {
            const data = await fs.readFile(process.argv[3]);
            const champions = JSON.parse(data);
            await generateChampionsVideos(champions, process.argv[3]);
            break;
        }
        case "generate-champions-videos-resume": {
            const data = await fs.readFile(process.argv[3]);
            const champions = JSON.parse(data);
            await generateChampionsVideos(champions, process.argv[3], true);
            break;
        }
        default: {
            throw new Error("Invalid command");
        }
    }
}

main();

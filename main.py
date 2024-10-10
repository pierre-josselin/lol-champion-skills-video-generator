import dotenv
import json
import moviepy.config
import moviepy.editor
import moviepy.video.fx
import os
import sys

dotenv.load_dotenv()

imageMagickBinaryPath = os.getenv("IMAGE_MAGICK_BINARY_PATH")
videoWidth = int(os.getenv("VIDEO_WIDTH"))
videoHeight = int(os.getenv("VIDEO_HEIGHT"))
videoFramerate = int(os.getenv("VIDEO_FRAMERATE"))
paddingSize = int(os.getenv("PADDING_SIZE"))
splashDuration = int(os.getenv("SPLASH_DURATION"))
splashChampionNameFontSize = int(os.getenv("SPLASH_CHAMPION_NAME_FONT_SIZE"))
splashChampionTitleFontSize = int(os.getenv("SPLASH_CHAMPION_TITLE_FONT_SIZE"))
splashChampionDescriptionFontSize = int(os.getenv("SPLASH_CHAMPION_DESCRIPTION_FONT_SIZE"))
abilityWithoutVideoDuration = int(os.getenv("ABILITY_WITHOUT_VIDEO_DURATION"))
abilityNameFontSize = int(os.getenv("ABILITY_NAME_FONT_SIZE"))
abilityDescriptionFontSize = int(os.getenv("ABILITY_DESCRIPTION_FONT_SIZE"))
abilityChampionNameFontSize = int(os.getenv("ABILITY_CHAMPION_NAME_FONT_SIZE"))
abilityImageWidth = int(os.getenv("ABILITY_IMAGE_WIDTH"))
abilityImageHeight = int(os.getenv("ABILITY_IMAGE_HEIGHT"))
championImageWidth = int(os.getenv("CHAMPION_IMAGE_WIDTH"))
championImageHeight = int(os.getenv("CHAMPION_IMAGE_HEIGHT"))
championImageCropSize = int(os.getenv("CHAMPION_IMAGE_CROP_SIZE"))
textColor = os.getenv("TEXT_COLOR")

championsDirectoryPath = os.path.join(".", "champions")

moviepy.config.change_settings({"IMAGEMAGICK_BINARY": imageMagickBinaryPath})

def main():
    with open(sys.argv[1], "r", encoding="utf8") as file:
        champions = json.load(file)

    clips = []
    for champion in champions:
        splashClips = []

        splashImagePath = os.path.join(championsDirectoryPath, champion["id"], "splash.jpg")
        splashImageClip = moviepy.editor.ImageClip(splashImagePath)
        splashImageClip = splashImageClip.set_duration(splashDuration)
        splashImageClip = splashImageClip.resize((videoWidth, videoHeight))
        splashClips.append(splashImageClip)

        splashChampionNameClip = moviepy.editor.TextClip(champion["name"], fontsize=splashChampionNameFontSize, color=textColor)
        splashChampionNameClip = splashChampionNameClip.set_duration(splashDuration)
        splashChampionNameClip = splashChampionNameClip.set_position((paddingSize, paddingSize))
        splashClips.append(splashChampionNameClip)

        splashChampionTitleClip = moviepy.editor.TextClip(champion["title"], fontsize=splashChampionTitleFontSize, color=textColor)
        splashChampionTitleClip = splashChampionTitleClip.set_duration(splashDuration)
        splashChampionTitleClip = splashChampionTitleClip.set_position((paddingSize, paddingSize + splashChampionNameClip.h + (paddingSize / 2)))
        splashClips.append(splashChampionTitleClip)

        splashChampionDescriptionClip = moviepy.editor.TextClip(champion["description"], fontsize=splashChampionDescriptionFontSize, color=textColor, align="West", method="caption", size=(splashImageClip.w / 2, None))
        splashChampionDescriptionClip = splashChampionDescriptionClip.set_duration(splashDuration)
        splashChampionDescriptionClip = splashChampionDescriptionClip.set_position((paddingSize, paddingSize + splashChampionNameClip.h + (paddingSize / 2) + splashChampionTitleClip.h + (paddingSize / 2)))
        splashClips.append(splashChampionDescriptionClip)

        splashClip = moviepy.editor.CompositeVideoClip(splashClips)
        clips.append(splashClip)

        for index, ability in enumerate(champion["abilities"]):
            abilityClips = []

            abilityVideoPathMp4 = os.path.join(championsDirectoryPath, champion["id"], "abilities", "videos", str(index) + ".mp4")
            abilityVideoPathWebm = os.path.join(championsDirectoryPath, champion["id"], "abilities", "videos", str(index) + ".webm")
            abilityVideoPath = abilityVideoPathMp4 if os.path.exists(abilityVideoPathMp4) else abilityVideoPathWebm if os.path.exists(abilityVideoPathWebm) else None

            if abilityVideoPath:
                abilityVideoClip = moviepy.editor.VideoFileClip(abilityVideoPath)
                abilityVideoClip = abilityVideoClip.resize((videoWidth, videoHeight))
                abilityClips.append(abilityVideoClip)
            else:
                abilityVideoClip = moviepy.editor.ColorClip(size=(videoWidth, videoHeight), color="black", duration=abilityWithoutVideoDuration)
                abilityClips.append(abilityVideoClip)

            championImagePath = os.path.join(championsDirectoryPath, champion["id"], "image.png")
            abilityChampionImageClip = moviepy.editor.ImageClip(championImagePath)
            abilityChampionImageClip = abilityChampionImageClip.set_duration(abilityVideoClip.duration)
            abilityChampionImageClip = abilityChampionImageClip.crop(x1=championImageCropSize, y1=championImageCropSize, x2=abilityChampionImageClip.w - championImageCropSize, y2=abilityChampionImageClip.h - championImageCropSize)
            abilityChampionImageClip = abilityChampionImageClip.resize(width=championImageWidth, height=championImageHeight)
            abilityChampionImageClip = abilityChampionImageClip.set_position((paddingSize, abilityVideoClip.h - abilityChampionImageClip.h - paddingSize))
            abilityClips.append(abilityChampionImageClip)

            abilityChampionNameClip = moviepy.editor.TextClip(champion["name"], fontsize=abilityChampionNameFontSize, color=textColor)
            abilityChampionNameClip = abilityChampionNameClip.set_duration(abilityVideoClip.duration)
            abilityChampionNameClip = abilityChampionNameClip.set_position((paddingSize + abilityChampionImageClip.w + paddingSize, abilityVideoClip.h - abilityChampionNameClip.h - paddingSize))
            abilityClips.append(abilityChampionNameClip)

            abilityNameClip = moviepy.editor.TextClip(ability["name"], fontsize=abilityNameFontSize, color=textColor)
            abilityNameClip = abilityNameClip.set_duration(abilityVideoClip.duration)
            abilityNameClip = abilityNameClip.set_position((paddingSize, paddingSize + abilityImageHeight + paddingSize))
            abilityClips.append(abilityNameClip)

            abilityDescriptionClip = moviepy.editor.TextClip(ability["description"], fontsize=abilityDescriptionFontSize, color=textColor, align="West", method="caption", size=((abilityImageWidth * len(champion["abilities"])) + (paddingSize * (len(champion["abilities"]) - 1)), None))
            abilityDescriptionClip = abilityDescriptionClip.set_duration(abilityVideoClip.duration)
            abilityDescriptionClip = abilityDescriptionClip.set_position((paddingSize, paddingSize + abilityImageHeight + paddingSize + abilityNameClip.h + (paddingSize / 2)))
            abilityClips.append(abilityDescriptionClip)

            for index2, ability in enumerate(champion["abilities"]):
                abilityImagePath = os.path.join(championsDirectoryPath, champion["id"], "abilities", "images", str(index2) + ".png")
                abilityImageClip = moviepy.editor.ImageClip(abilityImagePath)
                abilityImageClip = abilityImageClip.set_duration(abilityVideoClip.duration)
                abilityImageClip = abilityImageClip.resize(width=abilityImageWidth, height=abilityImageHeight)
                abilityImageClip = abilityImageClip.set_position(((paddingSize + (abilityImageWidth + paddingSize) * index2) if index2 > 0 else paddingSize, paddingSize))
                abilityImageClip = abilityImageClip.fx(moviepy.video.fx.all.blackwhite) if index != index2 else abilityImageClip
                abilityClips.append(abilityImageClip)

            abilityClip = moviepy.editor.CompositeVideoClip(abilityClips)
            clips.append(abilityClip)

    video = moviepy.editor.concatenate_videoclips(clips) # method="compose" if the clips are different sizes
    video.write_videofile(sys.argv[2], codec="libx264", fps=videoFramerate)

main()

import argparse
import os

import ffmpeg
import requests
import json
import inquirer

def download_json(id):
    url = "https://collegerama.tudelft.nl/Mediasite/PlayerService/PlayerService.svc/json/GetPlayerOptions"

    payload = {
        "getPlayerOptionsRequest": {
            "QueryString": "",
            "ResourceId": id,
            "UrlReferrer": "",
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def display_stream_info(streams):
    print(f"\n")
    for i, stream in enumerate(streams):
        print(f"Stream {i}:")
        print(f"\tId: {stream['Id']}")
        print(f"\tHasSlideContent: {stream['HasSlideContent']}")
        thumbnail_url = stream.get("ThumbnailUrl", "")
        if thumbnail_url:
            print("\tThumbnail URL:", f"https://collegerama.tudelft.nl{thumbnail_url}")
    print(f"\n")

def select_video_url(streams):
    answers = []
    for stream_nr, stream in enumerate(streams):

        has_slides = stream["HasSlideContent"]

        for i, video in enumerate(stream["VideoUrls"], start=1):
            mimetype = video["MimeType"]
            name =  f"Stream {stream_nr}, HasSlides: {has_slides}, MimeType: {mimetype}"
            option = {
                "StreamNr": stream_nr,
                "HasSlides": has_slides,
                "MimeType": mimetype,
                "DownloadUrl": video["Location"],
            }
            answers.append((name, option))

    questions = [
        inquirer.List("selected_video_url",
            message="Select video URL",
            choices=answers,
        ),
    ]

    answers = inquirer.prompt(questions)
    return answers["selected_video_url"]


def convert_to_filename(title):
    # return a name with the spaces replaced with "_" no unsupported characters for paths
    title = title.replace(" ", "_")
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c in ["_", "-", "(", ")"]]).rstrip()



def main():
    parser = argparse.ArgumentParser(description="Download JSON data from a URL")
    parser.add_argument("id", help="ID to include in the request URL")

    # Add the output_dir argument
    parser.add_argument(
        "--output-dir",
        help="Directory where the downloaded JSON file will be saved",
        default="Downloads",  # Set the default directory to "downloads"
    )

    args = parser.parse_args()
    id = args.id

    # Ensure the output directory exists or create it
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    json_data = download_json(id)
    if not json_data:
        print("Error: No JSON data found")
        return

    presentation_data = json_data.get("d", {}).get("Presentation", {})

    if not presentation_data:
        print("Error: No presentation data found")
        return

    print()
    title = presentation_data.get("Title", "")
    print(f"{title}\t {presentation_data.get('AirDate', '')} {presentation_data.get('AirTime', '')}")

    streams = presentation_data.get("Streams", [])

    if not streams:
        print("Error: No streams found")
        return

    display_stream_info(streams)
    selected_video = select_video_url(streams)

    # Output file name has Slides appended if the video has slides
    outputfile_name = f"{convert_to_filename(title)}{'_Slides' if selected_video['HasSlides'] else ''}.mp4"
    outputfile_path = os.path.join(output_dir, outputfile_name)
    outputfile_path = os.path.abspath(outputfile_path)

    download_url = selected_video["DownloadUrl"]
    print(f"Downloading video from : {download_url} to {outputfile_path}")

    # ffmpeg command
    # ffmpeg -protocol_whitelist file,http,https,tcp,tls -i [url] -c copy [full_path]
    input_kwargs = {
        "protocol_whitelist": "file,http,https,tcp,tls",
    }

    output_kwargs = {
        "c": "copy",
    }

    stream = ffmpeg.input(download_url, **input_kwargs)
    stream = ffmpeg.output(stream, outputfile_path, **output_kwargs)
    ffmpeg.run(stream)




if __name__ == "__main__":
    main()

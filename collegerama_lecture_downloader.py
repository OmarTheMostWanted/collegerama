import argparse
import os
import logging
from typing import List, Dict, Any, Optional

import ffmpeg
import requests
import json
import inquirer

def setup_logging(log_file: Optional[str] = None) -> None:
    """
    Sets up logging configuration. Logs to console by default, or to a file if specified.

    Args:
        log_file (Optional[str]): The file path to log to. If None, logs to console.
    """
    if log_file:
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_json(id: str) -> Optional[Dict[str, Any]]:
    """
    Downloads JSON data from the Collegerama service using the provided ID.

    Args:
        id (str): The resource ID to include in the request URL.

    Returns:
        Optional[Dict[str, Any]]: The JSON data as a dictionary if the request is successful, None otherwise.
    """
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
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching JSON data: {e}")
        return None

def display_stream_info(streams: List[Dict[str, Any]]) -> None:
    """
    Displays information about available streams.

    Args:
        streams (List[Dict[str, Any]]): A list of stream dictionaries containing stream information.
    """
    logging.info("Available Streams:")
    for i, stream in enumerate(streams):
        logging.info(f"Stream {i}:")
        logging.info(f"\tId: {stream['Id']}")
        logging.info(f"\tHasSlideContent: {stream['HasSlideContent']}")
        thumbnail_url = stream.get("ThumbnailUrl", "")
        if (thumbnail_url):
            logging.info(f"\tThumbnail URL: https://collegerama.tudelft.nl{thumbnail_url}")

def select_video_url(streams: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Prompts the user to select a video URL from the available streams.

    Args:
        streams (List[Dict[str, Any]]): A list of stream dictionaries containing stream information.

    Returns:
        Dict[str, Any]: The selected video URL information.
    """
    answers = []
    for stream_nr, stream in enumerate(streams):
        has_slides = stream["HasSlideContent"]
        for i, video in enumerate(stream["VideoUrls"], start=1):
            mimetype = video["MimeType"]
            name = f"Stream {stream_nr}, HasSlides: {has_slides}, MimeType: {mimetype}"
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

    selected = inquirer.prompt(questions)
    return selected["selected_video_url"]

def convert_to_filename(title: str) -> str:
    """
    Converts a title to a valid filename by replacing spaces with underscores and removing unsupported characters.

    Args:
        title (str): The title to convert.

    Returns:
        str: The converted filename.
    """
    title = title.replace(" ", "_")
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c in ["_", "-", "(", ")"]]).rstrip()

def download_video(download_url: str, outputfile_path: str) -> None:
    """
    Downloads a video from the given URL and saves it to the specified output file path.

    Args:
        download_url (str): The URL of the video to download.
        outputfile_path (str): The path where the downloaded video will be saved.
    """
    input_kwargs = {
        "protocol_whitelist": "file,http,https,tcp,tls",
    }
    output_kwargs = {
        "c": "copy",
    }
    stream = ffmpeg.input(download_url, **input_kwargs)
    stream = ffmpeg.output(stream, outputfile_path, **output_kwargs)
    ffmpeg.run(stream)

def main() -> None:
    """
    Main function to parse arguments and download the selected video.
    """
    parser = argparse.ArgumentParser(description="Download JSON data from a URL")
    parser.add_argument("id", help="ID to include in the request URL")
    parser.add_argument("--output-dir", help="Directory where the downloaded JSON file will be saved", default="Downloads")
    parser.add_argument("--log-file", help="File to log to. If not provided, logs to console.", default=None)
    args = parser.parse_args()

    setup_logging(args.log_file)

    os.makedirs(args.output_dir, exist_ok=True)

    json_data = download_json(args.id)
    if not json_data:
        logging.error("No JSON data found")
        return

    presentation_data = json_data.get("d", {}).get("Presentation", {})
    if not presentation_data:
        logging.error("No presentation data found")
        return

    title = presentation_data.get("Title", "")
    logging.info(f"{title}\t {presentation_data.get('AirDate', '')} {presentation_data.get('AirTime', '')}")

    streams = presentation_data.get("Streams", [])
    if not streams:
        logging.error("No streams found")
        return

    display_stream_info(streams)
    selected_video = select_video_url(streams)

    outputfile_name = f"{convert_to_filename(title)}{'_Slides' if selected_video['HasSlides'] else ''}.mp4"
    outputfile_path = os.path.join(args.output_dir, outputfile_name)
    outputfile_path = os.path.abspath(outputfile_path)

    logging.info(f"Downloading video from: {selected_video['DownloadUrl']} to {outputfile_path}")
    download_video(selected_video["DownloadUrl"], outputfile_path)

if __name__ == "__main__":
    main()
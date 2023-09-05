# Collegerama Lecture Downloader

This Python script allows you to download lecture videos from Collegerama. It is a complete overhaul of the old downloader, which can be found in the branch [old-downloader](../../tree/old_downloader).

## Table of Contents
- [Installation](#installation)
  - [Windows](#windows)
  - [Mac](#mac)
  - [Linux](#linux)
- [Usage](#usage)

---

## Installation

### Windows

1. **Python Installation:** If you don't have Python installed, download and install it from the official [Python website](https://www.python.org/downloads/).

2. **WSL (Windows Subsystem for Linux):** For Windows users, you can use Windows Subsystem for Linux (WSL) to run the script. If you haven't already, follow the instructions to [install WSL](https://docs.microsoft.com/en-us/windows/wsl/install).

3. **FFmpeg Installation:** Inside your WSL terminal, install FFmpeg using the package manager:
   ```bash
   sudo apt-get install ffmpeg
   ```
4. **Clone Repository:** In your WSL terminal, clone the repository using Git:
    ```bash
    git clone https://github.com/djosh34/collegerama.git
   cd collegerama
    ```
   
5. **Install Dependencies:** In your WSL terminal, install the required Python dependencies using pip:
    ```bash
    pip install requests inquirer ffmpeg-python
    ```

### Mac

1. **Python Installation:** Python should already be installed on Mac. If you don't have Python installed, download and install it from the official [Python website](https://www.python.org/downloads/).
2. **Install Homebrew:** Install Homebrew using the instructions on the [Homebrew website](https://brew.sh/).
3. **FFmpeg Installation:** Install FFmpeg using Homebrew in your terminal:
   ```bash
   brew install ffmpeg
   ```
4. **Clone Repository:** In your terminal, clone the repository using Git:
    ```bash
    git clone https://github.com/djosh34/collegerama.git
    cd collegerama
     ```
5. **Install Dependencies:** In your terminal, install the required Python dependencies using pip:
    ```bash
    pip install requests inquirer ffmpeg-python
    ```
### Linux
1. **Linux Install notes:**

    Since you're using linux, you're already an extreme pro and know how installing stuff like this works. 
 
    For this script you need to have the following installed:
    - Any version of python 3 which is compatible with inquirer and ffmpeg-python
    - ffmpeg
    - git

2. **Clone Repository:** In your terminal, clone the repository using Git:
    ```bash
    git clone https://github.com/djosh34/collegerama.git
    cd collegerama
    ```

3. **Install Dependencies:** In your terminal, install the required Python dependencies using pip:
    ```bash
    pip install requests inquirer ffmpeg-python
    ```

## Usage

1. **Navigate to the Script Directory:** In your terminal (WSL for Windows users), navigate to the script's directory 

    ```bash
    cd path/to/collegerama
    ```

2. **Run the Script:** Use the following command to run the script, replacing `<ID>` with the lecture's ID you want to download:

   ```bash
   python collegerama_lecture_downloader.py <ID>
   ```

   You can also specify an optional `--output-dir` argument to specify the directory where the downloaded video will be saved. If not provided, it will default to a "Downloads" directory within the script folder.

   Example with an output directory specified:

    ```bash
   python collegerama_lecture_downloader.py <ID> --output-dir /path/to/your/directory
    ```

3. **Select Video:** The script will display available video streams, allowing you to select the one you want to download.
   Videos with the MimeType `video/mp4` are recommended, as they are the most stable when downloading

4. **Download:** The selected video will be downloaded to your specified or default output directory.

Please note that this script relies on external libraries and Collegerama's website structure, which may change over time. If you encounter issues, make sure the script is up to date and report any problems to the script's repository.

Enjoy downloading Collegerama lectures!
    
# Image Caption Editor

A user-friendly desktop application built with Python and Gradio that allows you to view images and edit their associated captions. The application saves captions as text files alongside the images.

## Features

- Browse and load folders containing PNG images
- Navigate through images with Previous/Next buttons
- View images and edit their captions
- Save captions as .txt files (same name as the image)
- Jump to specific images by number
- Native folder selection dialog for different operating systems
- Clear all fields functionality
- Status updates for all operations

## Prerequisites

- Python 3.9 or higher
- Required Python packages:
  ```bash
  pip install gradio
  ```

For Linux users, one of the following dialog utilities is required:
- zenity (recommended): `sudo apt-get install zenity`
- kdialog: Usually included with KDE desktop environment

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
   ```bash
   pip install gradio
   ```

## Usage

1. Run the script:
   ```bash
   python mainframe.py
   ```

2. The application will launch in your default web browser
3. Click "Browse..." to select a folder containing PNG images
4. Navigate through images using the Previous/Next buttons
5. Edit captions in the text box
6. Click "Save Caption" to save changes
7. Use "Jump to Image #" to navigate to a specific image
8. Click "Clear All Fields" to reset the application

## File Structure

For each image file (`example.png`), the application creates or updates a corresponding text file (`example.txt`) in the same directory containing the caption.

## Supported Operating Systems

- Windows
- macOS
- Linux (requires zenity or kdialog)

## Security

The application restricts file access to common user directories:
- Downloads folder
- Desktop folder

## License

[Add your chosen license here]

## Contributing

[Add contribution guidelines if applicable]

import gradio as gr
import os
from pathlib import Path
import glob
from PIL import Image

class ImageCaptionEditor:
    """
    Class to manage the state and operations of the image caption editor
    """
    def __init__(self):
        self.image_files = []  # List to store image file paths
        self.current_index = 0  # Index to keep track of the current image
        self.folder_path = None  # Path to the folder containing images
    

    def get_current_pair(self):
        """
        Retrieve the current image path and its corresponding caption
        Returns: tuple(image_path, caption, status_message)
        """
        if not self.image_files:
            return None, "", "No images loaded"
        
        image_path = self.image_files[self.current_index]
        txt_path = image_path.replace('.png', '.txt')
        
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                caption = f.read().strip()
        except FileNotFoundError:
            caption = ""
            
        return image_path, caption, f"Showing image {self.current_index + 1} of {len(self.image_files)}"


    def load_folder(self, folder_path):
        """Load all PNG files from the specified folder"""
        if not folder_path:  # Check if no folder path is provided
            return None, "", "No folder selected"
        
        if isinstance(folder_path, list):  # Check if folder_path is a list
            folder_path = folder_path[0]  # Use the first element of the list
        elif isinstance(folder_path, dict):  # Check if folder_path is a dictionary
            folder_path = folder_path['path']  # Use the 'path' key from the dictionary
        
        self.folder_path = folder_path  # Set the folder path
        self.image_files = sorted(glob.glob(os.path.join(folder_path, "*.png")))  # Get all PNG files in the folder
        
        if not self.image_files:  # Check if no images are found
            return None, "", "No PNG files found in the selected folder"
        
        self.current_index = 0  # Reset the current index
        return self.get_current_pair()  # Return the first image details

    
    def next_pair(self, _):
        """Move to next image if available"""
        if self.current_index < len(self.image_files) - 1:  # Check if there is a next image
            self.current_index += 1  # Increment the current index
        return self.get_current_pair()  # Return the next image details

    
    def previous_pair(self, _):
        """Move to previous image if available"""
        if self.current_index > 0:  # Check if there is a previous image
            self.current_index -= 1  # Decrement the current index
        return self.get_current_pair()  # Return the previous image details

    
    def save_caption(self, caption):
        """Save the caption to a text file"""
        if not self.image_files:
            return None, caption, "No images loaded"
        
        current_image = self.image_files[self.current_index]
        txt_path = current_image.replace('.png', '.txt')
        
        try:
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(caption)
            return current_image, caption, f"Caption saved for image {self.current_index + 1}"
        except Exception as e:
            return current_image, caption, f"Error saving caption: {str(e)}"

    def clear_all(self):
        """Clear all loaded data and reset the editor state"""
        self.image_files = []
        self.current_index = 0
        self.folder_path = None
        return None, "", "All fields cleared", ""


def create_interface():
    """
    Create and configure the Gradio interface
    """
    editor = ImageCaptionEditor()
    
    with gr.Blocks() as interface:
        # Header
        gr.Markdown("# Image Caption Editor")
        
        # Folder input and buttons section
        with gr.Column():
            with gr.Row():
                folder_input = gr.Textbox(
                    label="Enter or paste folder path",
                    placeholder="e.g., /path/to/your/images/folder",
                    scale=3
                )
                with gr.Column():
                    load_btn = gr.Button("Load Folder")
                    clear_btn = gr.Button("Clear All Fields")
        
        # Image and caption section side by side
        with gr.Row():
            image_output = gr.Image(
                type="filepath",
                label="Image",
                width="500px",
                scale=1
            )
            caption_input = gr.Textbox(
                label="Caption", 
                lines=3,
                scale=1
            )
        
        # Navigation and save buttons
        with gr.Row():
            prev_btn = gr.Button("← Previous")
            next_btn = gr.Button("Next →")
            save_btn = gr.Button("Save Caption")
        
        # Status display
        status_output = gr.Textbox(label="Status", interactive=False)
        
        # Connect UI elements to their corresponding functions
        load_btn.click(
            fn=editor.load_folder,
            inputs=[folder_input],
            outputs=[image_output, caption_input, status_output]
        )
        
        next_btn.click(
            fn=editor.next_pair,
            inputs=[caption_input],
            outputs=[image_output, caption_input, status_output]
        )
        
        prev_btn.click(
            fn=editor.previous_pair,
            inputs=[caption_input],
            outputs=[image_output, caption_input, status_output]
        )
        
        save_btn.click(
            fn=editor.save_caption,
            inputs=[caption_input],
            outputs=[image_output, caption_input, status_output]
        )
        
        clear_btn.click(
            fn=editor.clear_all,
            inputs=[],
            outputs=[image_output, caption_input, status_output, folder_input]
        )
    
    return interface


# Only run the interface if this file is run directly
if __name__ == "__main__":
    # Get user's home directory
    home = str(Path.home())
    
    # Define common macOS paths
    allowed_paths = [
        os.path.join(home, "Downloads"),
        os.path.join(home, "Desktop")
    ]
    
    interface = create_interface()
    interface.launch(allowed_paths=allowed_paths)

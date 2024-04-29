from pathlib import Path
from flask import current_app # Info regarding application
from uuid import uuid4

class ImageHandler:

    # Saves the image to disk with a unique name and returns that unique name:
    @staticmethod
    def save_image(file_name):
        if not file_name.filename: return None
        suffix = Path(file_name.filename).suffix # Extract original suffix .
        image_name = str(uuid4()) + suffix # Create unique name + original suffix 
        image_path = Path(current_app.root_path) / "static/images/vacations_landscapes" / image_name # Get image path
        file_name.save(image_path) # Saving the image to disk.
        return image_name # Returning only the image name (including suffix).

    # Update existing image:
    @staticmethod
    def update_image(old_image_name, file_name):
        if not file_name.filename: return old_image_name # Return old file_name if no image.
        image_name = ImageHandler.save_image(file_name) # Save new image with a new name
        ImageHandler.delete_image(old_image_name) # Delete old image
        return image_name # Return new name

    # Delete existing image: 
    @staticmethod
    def delete_image(file_name): 
        if not file_name: return # Do nothing if no image
        image_path = Path(current_app.root_path) / "static/images/vacations_landscapes" / file_name # Get image path
        image_path.unlink(missing_ok = True) # Delete image from disk, don't crash if file not exist.

    # Return image absolute path from image name: 
    @staticmethod
    def get_image_path(file_name):
        # current_app.root_path is the path for the src folder
        image_folder = Path(current_app.root_path) / "static/images/vacations_landscapes"
        image_path = image_folder / file_name
        if not image_path.exists(): 
            image_path =  Path(current_app.root_path) / "static/images/no_image.png"
        return image_path


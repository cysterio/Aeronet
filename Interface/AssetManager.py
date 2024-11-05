import os
from PIL import Image

class AssetManager:
    @staticmethod
    def get_asset_path(filename: str) -> str:
        return os.path.join(os.path.dirname(__file__), 'Assets', filename)
    
    @staticmethod
    def load_image(filename: str) -> Image.Image:
        path = AssetManager.get_asset_path(filename)
        try:
            return Image.open(path)
        except FileNotFoundError:
            print(f"Warning: Could not find image file at {path}")
            raise

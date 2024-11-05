import tkinter as tk

from PIL import Image, ImageTk
from Interface.AssetManager import AssetManager

class RadarCanvas(tk.Canvas):
    def __init__(self, master: tk.Tk, *args: tuple, **kwargs: dict) -> None:
        super().__init__(master, *args, **kwargs)
        self.images_on_canvas: list[ImageTk.PhotoImage] = []
    
    def check_event(self, event: tk.Event, item: str) -> bool:
        x1, y1, x2, y2 = self.bbox(item)
        return x1 <= event.x <= x2 and y1 <= event.y <= y2
    
    def draw_plane_icon(self, cw: float, ch: float, fcode: str, hdg: float, ord: tuple[float, float]) -> None:
        true_x: float = cw + ord[0]
        true_y: float = ch - ord[1]
        
        try:
            photo: Image.Image = AssetManager.load_image('plane_icon.png')
            plane: Image.Image = photo.rotate(-hdg + 45)
            image_on_canvas: ImageTk.PhotoImage = ImageTk.PhotoImage(plane)
            self.create_image(true_x, true_y, image=image_on_canvas, tag=f"{fcode} aircraft")
            self.images_on_canvas.append(image_on_canvas)
        except Exception as e:
            ...
    
    def clear_images(self) -> None:
        for image in self.images_on_canvas:
            self.delete(image)
        self.images_on_canvas.clear()
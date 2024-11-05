import math
import random

import tkinter as tk
from PIL import Image, ImageTk

from Utils.Update.WeatherUtils import Weather
from Utils.Update.FlightPathUtils import FlightPath
from Utils.Update.FM_DataUtils import FM_Data
from Utils.Logic.WaypointUtils import WaypointUtils

from Interface.Blocs.RadarCanvas import RadarCanvas
from Interface.AssetManager import AssetManager

class Radar:
    hover_fno: str = "hover_plane"
    
    def __init__(self, root: tk.Tk) -> None:
        self.window: tk.Tk = root
        
        self.canvas_width: int = 390
        self.canvas_height: int = 375
        
        self.radar_radius: int = 155

        self.can: RadarCanvas = RadarCanvas(self.window, width=self.canvas_width, height=self.canvas_height, bg="#232324")
        self.can.grid(row=0, column=0, rowspan=15, padx = (10, 10), pady=(15, 8), sticky = 'nw')
        self.can.bind('<Button-1>', self.hover)
        
        self.draw_radar_grid(self.canvas_width//2, self.canvas_height//2, self.radar_radius, 25, "green")
        self.draw_headings(self.canvas_width//2, self.canvas_height//2, self.radar_radius, "#14fE64")
        self.draw_distances(self.canvas_width//2, self.canvas_height//2, 25, "#14fE64")
        self.print_weather_data(self.canvas_width, self.canvas_height, "yellow")
        
    def draw_radar_grid(self, x: int, y: int, r: int, wd: int, color: str) -> None:
        self.can.create_oval(x-r, y-r, x+r, y+r, width=2, outline=color, fill = "#232324")
        for i in range(r//wd):
            self.can.create_oval(x-r+i*wd, y-r+i*wd, x+r-i*wd, y+r-i*wd, width=2, outline=color)
        self.can.create_line(x-r,y,x+r,y,fill=color)
        self.can.create_line(x,y-r,x,y+r,fill=color)
        
    def draw_headings(self, cw: int, ch: int, r: int, color: str) -> None:
        for i in range(0, 360, 10):
            f: int = r + len(str(i)) + 10
            x: float = cw + f * math.cos((i - 90) * math.pi / 180)
            y: float = ch + f * math.sin((i - 90) * math.pi / 180)
            self.can.create_text(x, y, text=f'{i}', fill=color)
            
    def draw_distances(self, cw: int, ch: int, wd: int, color: str) -> None:
        for i in range(1, 4):
            self.can.create_text(cw+i*2*wd-2.5*len(str(10*i))-4, ch-7, text=str(10*i), fill=color)
            
    def print_weather_data(self, cw: int, ch: int, color: str) -> None:
        data: list = [Weather.description(),
                      Weather.precipitation(),
                      Weather.wind_speed(),
                      Weather.cloud_base(),
                      FlightPath.count_traffic()]
        
        while self.can.find_withtag('weather'):
            self.can.delete('weather')
        while self.can.find_withtag('traffic'):
            self.can.delete('traffic')
        
        self.can.create_text(5, 5, text=f"{data[0]}", anchor="nw", fill=color, tags="weather")
        self.can.create_text(5, 20, text=f"{data[1]}%, {data[2]}kts",anchor="nw", fill=color, tags="weather")
        self.can.create_text(5, 35, text=f"{data[3]}m", anchor="nw", fill=color, tags="weather")
        
        traffic: str = "Good" if data[4] <= 4 else "Moderate" if data[4] <= 7 else "Extreme"
        
        self.can.create_text(cw-5, ch-35, text="Air Traffic", anchor="se", fill=color, tags="traffic")
        self.can.create_text(cw-5, ch-20, text=f"{data[4]:02d}/10",anchor="se", fill=color, tags="traffic")
        self.can.create_text(cw-5, ch-5, text=f"{traffic}", anchor="se", fill=color, tags="traffic")
    
    def print_flightdata(self, color: str) -> None:
        cw: int = self.canvas_width
        ch: int = self.canvas_height
        
        fnos: list = FM_Data.get_all_fno()
        
        while self.can.find_withtag('fdata'):
            self.can.delete('fdata')
        
        if Radar.hover_fno not in fnos:
            return
        
        if FM_Data.altitude(Radar.hover_fno) <= 16:
            return 
        flight_data: list = [Radar.hover_fno, 
                            FM_Data.altitude(Radar.hover_fno), 
                            FM_Data.air_speed(Radar.hover_fno)]
        
        flight_data[2] = random.choice(range(flight_data[2]-2, flight_data[2]+2))
        
        flight_path: str = FlightPath.waypoints(Radar.hover_fno)
        waypoints: list = flight_path.split('~')

        path_data: list = [round(WaypointUtils.track_miles(Radar.hover_fno),2),
                            FlightPath.rate_assign(Radar.hover_fno),
                            waypoints[0]
                            ]
        
        if len(waypoints) == 1:
            path_data[2] = "EXT"
        if waypoints[0].replace(" ", "") == "(0,0)":
            path_data[2] = "RWY"

        self.can.create_text(cw-5, 5, text=f"{flight_data[0]}", anchor="ne", fill=color, tags= 'fdata')
        self.can.create_text(cw-5, 20, text=f"{flight_data[1]}m",anchor="ne", fill=color, tags= 'fdata')
        self.can.create_text(cw-5, 35, text=f"{flight_data[2]}kts", anchor="ne", fill=color, tags= 'fdata')

        self.can.create_text(5, ch-35, text=f"{path_data[0]}", anchor="sw", fill=color, tags= 'fdata')
        self.can.create_text(5, ch-20, text=f"{path_data[1]}",anchor="sw", fill=color, tags= 'fdata')
        self.can.create_text(5, ch-5, text=f"{path_data[2]}", anchor="sw", fill=color, tags= 'fdata')
                
    def hover(self, event: tk.Event) -> None:
        target: int = event.widget.find_closest(event.x, event.y)[0]
        tag: str = self.can.itemcget(target, "tag").split()
        
        try:
            if self.can.check_event(event, target):
                if Radar.hover_fno == tag[0]:
                    Radar.hover_fno = 'hover_plane'
                    for i in ('path', 'wayp', 'fdata'):
                        while self.can.find_withtag(i):
                            self.can.delete(i)
                    return
                
                if tag[1] == 'aircraft':
                    Radar.hover_fno = tag[0]
                    return
        except IndexError:
            pass
    
    def draw_planes(self) -> None:
        fnos: list = FM_Data.get_all_fno()
        can_items: list = self.can.find_all()
    
        for item in can_items:
            tags: list = self.can.gettags(item)
            
            if any(tag.split()[-1] == "aircraft" for tag in tags):
                self.can.delete(item)
        
        for fcode in fnos:
            coords: tuple = FM_Data.coordinates(fcode)
            hdg: int = FM_Data.heading(fcode)
            
            if FM_Data.altitude(fcode) > 16:
                self.can.draw_plane_icon(self.canvas_width//2, self.canvas_height//2, fcode, hdg, coords)
        self.can.update()

    def draw_flightpath(self, colors: list) -> None:
        fnos: list = FM_Data.get_all_fno()
        
        if not Radar.hover_fno in fnos:
            while self.can.find_withtag('path'):
                self.can.delete('path')
            return
            
        if FM_Data.altitude(Radar.hover_fno) > 16:
            while self.can.find_withtag('path'):
                self.can.delete('path')
            
            flight_path: str = FlightPath.waypoints(Radar.hover_fno)
            waypoints: list = flight_path.split('~')
            
            x: int = FM_Data.coordinates(Radar.hover_fno)[0]
            y: int = FM_Data.coordinates(Radar.hover_fno)[1]
            path_coords: list = [self.canvas_width//2 + x, self.canvas_height//2 - y]
            
            for waypoint in waypoints:
                wp_x: int = WaypointUtils.get_waypoint_coords(waypoint)[0]
                wp_y: int = WaypointUtils.get_waypoint_coords(waypoint)[1]
                
                path_coords.extend([
                    self.canvas_width//2 + wp_x,
                    self.canvas_height//2 - wp_y
                ])
                
                if (wp_x, wp_y) == (0,0):
                    break
            
            if len(path_coords) >= 4:
                rate: str = FlightPath.rate_assign(Radar.hover_fno)
                match rate:
                    case "Slow":
                        color: str = colors[0]
                    case "Steady":
                        color: str = colors[1]
                    case "Fast":
                        color: str = colors[2]
                        
                self.can.create_line(path_coords, fill=color, tags="path", smooth=False)
        else:
            while self.can.find_withtag('path'):
                self.can.delete('path')
            
    def draw_waypoints(self, can_x: int, can_y: int) -> None:
        while self.can.find_withtag('wayp'):
                self.can.delete('wayp')
        
        if Radar.hover_fno == "hover_plane":
            return
        
        if Radar.hover_fno not in FM_Data.get_all_fno():
            Radar.hover_fno == "hover_plane"
            return
        
        waypoints: list = FlightPath.waypoints(Radar.hover_fno).split("~")
        del waypoints[-1]
        
        self.images_on_canvas: list = []
        for i in waypoints:
            if i  == "(0, 0)":
                break
            
            wp_x: int = WaypointUtils.get_waypoint_coords(i)[0]
            wp_y: int = WaypointUtils.get_waypoint_coords(i)[1]
            wp_truex: int = can_x + wp_x
            wp_truey: int = can_y - wp_y
            
            photo: Image.Image = AssetManager.load_image('waypoint.png')
            image_on_canvas: ImageTk.PhotoImage = ImageTk.PhotoImage(photo)
            self.can.create_image(wp_truex, wp_truey, image=image_on_canvas, tags="wayp")
            self.images_on_canvas.append(image_on_canvas)

import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk

from Interface.Panels.Radar import Radar as Radar_Panel
from Interface.Panels.Spawn import Spawn as Spawn_Panel
from Interface.Panels.Logger import Logger as Log_Panel
from Interface.Blocs.AnimateUtils import AnimateUtils

from Utils.Update.FM_DataUtils import FM_Data
from Utils.Update.FlightPathUtils import FlightPath
from Utils.Update.ScheduleUtils import Schedule

from Utils.Logic.WeatherUpdate import WeatherUpdate
from Utils.Logic.WaypointUtils import WaypointUtils
from Utils.Logic.AntiCollision import AntiCollision
from Utils.Logic.Sequencing import Sequencing

from Interface.AssetManager import AssetManager

class Interface:
    def __init__(self) -> None:
        self.mainWindow: tk.Tk = tk.Tk()
        self.mainWindow.title("Aeronet")
        
        def on_closing() -> None:
            if messagebox.askquestion("Exit Box", "Do you want to exit Aeronet ???") == 'yes':
                sys.exit(0)
        
        icon_image = AssetManager.load_image("icon.jpg")
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.mainWindow.iconphoto(False, icon_photo)
        
        self.mainWindow.protocol("WM_DELETE_WINDOW", on_closing)
        self.mainWindow.config(background="#606060", highlightcolor="black")
        self.mainWindow.minsize(630, 408)
        self.mainWindow.maxsize(630, 408)
        
        def center_window(window: tk.Tk, width: int, height: int) -> None:
            screen_width: int = window.winfo_screenwidth()
            screen_height: int = window.winfo_screenheight()
            window_width: int = width
            window_height: int = height
            
            x: int = (screen_width - window_width) // 2
            y: int = (screen_height - window_height) // 2
            
            window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        center_window(self.mainWindow, width=630, height=408)
        
        self.logger: Log_Panel = Log_Panel(self.mainWindow)
        self.spawn: Spawn_Panel = Spawn_Panel(self.mainWindow, self.logger)
        self.radar: Radar_Panel = Radar_Panel(self.mainWindow)

        WeatherUpdate.auto_update()
        self.radar.print_weather_data(self.radar.canvas_width, self.radar.canvas_height, "yellow")
        
        self.delay: int = 200
        self.update_()
        
        self.mainWindow.focus_force()
        self.mainWindow.mainloop()
        
    def update_(self) -> None:
        WeatherUpdate.auto_update()
        
        fnos: list[str] = FM_Data.get_all_fno()
        
        for fcode in fnos:
            if fcode in Sequencing.landing_fno:
                if Schedule.check_schedule(fcode):
                    Sequencing.take_off_fno.append(fcode)
                    Sequencing.landing_fno.remove(fcode)
            if fcode in Sequencing.take_off_fno:
                if Sequencing.check_landing_traffic(fcode) and Sequencing.rwy_available:
                    Sequencing.take_off_aircraft(fcode)
                    self.logger.log(f"{fcode} took off from Airport", "yellow")
            
            exists: bool = True
            coords: tuple[float, float] = FM_Data.coordinates(fcode)
            steps: tuple[float, float] = AnimateUtils.get_coord_step(fcode, coords)
            
            updated_coords: tuple[float, float] = (float(coords[0] + steps[0]), float(coords[1] + steps[1]))
            FM_Data.coordinates(fcode, updated_coords)
            
            for _ in range(2):
                path: list[str] = FlightPath.waypoints(fcode).split('~')
                dist: float = WaypointUtils.dist_from_waypoint(updated_coords, path[0])
                
                if dist <= 0.3:
                    if path[0] == "(0, 0)" or FM_Data.altitude(fcode) < 16:
                        if fcode not in Sequencing.landing_fno:
                            Sequencing.land_aircraft(fcode)
                            self.logger.log(f"{fcode} landed at Airport", "yellow")
                        
                        if Radar_Panel.hover_fno == fcode:
                            Radar_Panel.hover_fno = "hover_plane"
                            
                        exists = False
                        break
                
                    if len(path) == 1:
                        FM_Data.remove_flight_data(fcode)
                        FlightPath.remove_flight_path(fcode)
                        self.logger.log(f"{fcode} leaving Airspace")
                        
                        exists = False
                        break
                    
                    path = "~".join(path[1:])
                    FlightPath.waypoints(fcode, path)
            
            if exists and FM_Data.altitude(fcode) > 16:
                FlightPath.dist_from_waypoint(fcode, dist)
                
                nxt_hdg: int = WaypointUtils.find_nxt_heading(coords, updated_coords)
                FM_Data.heading(fcode, nxt_hdg)
                
                alt: float = FM_Data.altitude(fcode)
                nxt_alt: float = alt + AnimateUtils.get_altitude_step(fcode, coords, alt)
                FM_Data.altitude(fcode, nxt_alt)
                
                spd: float = FM_Data.air_speed(fcode)
                nxt_spd: float = spd + AnimateUtils.get_airspeed_step(fcode, spd)
                FM_Data.air_speed(fcode, nxt_spd)
        
        if Sequencing.rwy_available < 0:
            Sequencing.rwy_available += 1
        else:
            Sequencing.rwy_available = True 
            
        AntiCollision.fix_conflict(AntiCollision.conflict_possibilities())
        Sequencing.fix_landing_collisions()
        
        self.animate_()
    
    def animate_(self) -> None:
        self.radar.print_weather_data(self.radar.canvas_width, self.radar.canvas_height, "yellow")
        
        self.radar.draw_flightpath(["Blue", "yellow", "Red"])
        self.radar.print_flightdata("yellow")
        
        self.radar.draw_waypoints(self.radar.canvas_width//2, self.radar.canvas_height//2)
        self.radar.draw_planes()
        
        self.radar.can.update()
        self.mainWindow.update()
        
        self.mainWindow.after(self.delay, self.update_)
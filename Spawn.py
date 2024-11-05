import tkinter as tk
from tkinter import ttk

from Interface.Panels.Radar import Radar
from Utils.Logic.ValidateInput import EntryCheck
from Utils.Logic.WaypointUtils import WaypointUtils
from Utils.Logic.OptimalFlightPath import OptimumPath
from Utils.Update.FM_DataUtils import FM_Data
from Utils.Update.FlightPathUtils import FlightPath

class Spawn:
    def __init__(self, root: tk.Tk, logger) -> None:
        self.window: tk.Tk = root
        self.logger = logger
        self.frame: tk.Frame = tk.Frame(root, width=405, height=148, background="#606060")
        self.frame.grid(row=0, column=1, rowspan=12, padx=0, pady=(8, 5), sticky="n")
        
        fl_entry_label: tk.Label = tk.Label(self.frame, text=f'{"─"*6}  FLIGHT ENTRY  {"─"*6}', 
                                             font=("", 9, "bold"), fg="black", bg="#606060")
        fl_entry_label.grid(row=0, column=0, columnspan=9, padx=(2, 0), sticky="nw")
        
        self.draw_fno_cell()
        self.draw_hdg_cell()
        self.draw_alt_cell()
        self.draw_spd_cell()
        self.draw_wyp_cell()
        self.draw_land_cell()
        self.draw_rno_cell()
        self.draw_clr_btn()
        self.draw_add_flight_btn()
        
    def draw_fno_cell(self) -> None:
        self.fno_label: tk.Label = tk.Label(self.frame, text="Enter flight code : ", fg="black", bg="#606060")
        self.fno_label.grid(row=1, column=0, sticky="w", pady=(8, 0), columnspan=3)
        
        self.fno_entry: tk.Entry = tk.Entry(self.frame, text="", bg="white", border=1)
        self.fno_entry.config(width=14)
        self.fno_entry.grid(row=1, column=4, columnspan=4, sticky="w", pady=(5, 0))
    
    def draw_hdg_cell(self) -> None:
        self.hdg_label: tk.Label = tk.Label(self.frame, text="Enter heading : ", fg="black", bg="#606060")
        self.hdg_label.grid(row=3, column=0, columnspan=4, sticky="w", pady=(5, 0))
        
        self.hdg: tk.StringVar = tk.StringVar()
        self.hdg_spin: tk.Spinbox = tk.Spinbox(self.frame, from_=0, to=359, increment=1, textvariable=self.hdg, fg="black", bg="white")
        self.hdg_spin.configure(width=12)
        self.hdg_spin.grid(row=3, column=4, columnspan=4, sticky="w", pady=(5, 0))
        
    def draw_alt_cell(self) -> None:
        self.alt_label: tk.Label = tk.Label(self.frame, text="Enter altitude : ", fg="black", bg="#606060")
        self.alt_label.grid(row=4, column=0, columnspan=4, sticky="w", pady=(5, 0))
        
        self.alt: tk.StringVar = tk.StringVar(value=3000)
        self.alt_spin: tk.Spinbox = tk.Spinbox(self.frame, from_=2500, to=5000, increment=50, textvariable=self.alt, fg="black", bg="white")
        self.alt_spin.configure(width=12)
        self.alt_spin.grid(row=4, column=4, sticky="w", pady=(5, 0), columnspan=4)
        
    def draw_spd_cell(self) -> None:
        self.spd_label: tk.Label = tk.Label(self.frame, text="Enter airspeed : ", fg="black", bg="#606060")
        self.spd_label.grid(row=5, column=0, columnspan=4, sticky="w", pady=(5, 0))
        
        self.spd: tk.StringVar = tk.StringVar(value=180)
        self.spd_spin: tk.Spinbox = tk.Spinbox(self.frame, from_=150, to=200, increment=5, textvariable=self.spd, fg="black", bg="white")
        self.spd_spin.configure(width=12)
        self.spd_spin.grid(row=5, column=4, columnspan=4, pady=(5, 0), sticky="w")
    
    def draw_wyp_cell(self) -> None:
        self.wyp_label: tk.Label = tk.Label(self.frame, text="Enter waypoint : ", fg ="black", bg="#606060")
        self.wyp_label.grid(row=6, column=0, columnspan=4, sticky="w", pady=(5, 0))
        
        self.waypoints: list = list(WaypointUtils.fetch_waypoints()["Primary"].keys())
        self.wayp_menu: ttk.Combobox = ttk.Combobox(self.frame, values=self.waypoints, state="readonly")
        self.wayp_menu.set(self.waypoints[0])
        self.wayp_menu.config(width=12)
        self.wayp_menu.grid(row=6, column=4, columnspan=2, sticky="w", pady=(5, 0))
    
    def toggle_landing(self) -> None:
        try:
            self.ded_hdg_label.destroy()
            self.ded_hdg_spin.destroy()
            
            self.rno_label.destroy()
            self.rno_menu.destroy()
        except AttributeError:
            try:
                self.rno_label.destroy()
                self.rno_menu.destroy()
                
                self.ded_hdg_label.destroy()
                self.ded_hdg_spin.destroy()
            except AttributeError:
                ...
        
        if self.landing.get():
            self.draw_rno_cell()
            self.window.update()
        else:
            self.draw_ded_hdg_cell()
            self.window.update()
    
    def draw_land_cell(self) -> None:
        self.landing: tk.BooleanVar = tk.BooleanVar(value=True)
        
        self.land_check_1: tk.Radiobutton = tk.Radiobutton(self.frame, text="Yes", variable=self.landing, font=("",10), bg="#606060", activebackground="#606060", command=self.toggle_landing, value=True)
        self.land_check_2: tk.Radiobutton = tk.Radiobutton(self.frame, text="No", variable=self.landing, font=("",10), bg="#606060", activebackground="#606060", command=self.toggle_landing, value=False)
        self.land_check_1.grid(row=7, column=3, columnspan=3, sticky="w", padx=(3,0), pady=(5,0))
        self.land_check_2.grid(row=7, column=5, columnspan=3, sticky="w", padx=(0, 0), pady=(5,0))
        
        self.land_label: tk.Label = tk.Label(self.frame, text="Land on Runway : ", fg="black", bg="#606060")
        self.land_label.grid(row=7, column=0, columnspan=4, pady=(5,0), sticky="w")
        
    def draw_rno_cell(self) -> None:
        self.rno_label: tk.Label = tk.Label(self.frame, text="Runway Number : ", fg="black", bg="#606060")
        self.rno_label.grid(row=8, column=0, columnspan=4, pady=(5,0), sticky="w")
        
        self.rno_menu: ttk.Combobox = ttk.Combobox(self.frame, values=["09 L", "27 R"], state="readonly")
        self.rno_menu.set("09 L")
        self.rno_menu.config(width=10)
        self.rno_menu.grid(row=8, column=4, columnspan=4, sticky="w", pady=(5,0))
    
    def draw_ded_hdg_cell(self) -> None:
        self.ded_hdg_label: tk.Label = tk.Label(self.frame, text="Route Heading :  \t ", fg="black", bg="#606060")
        self.ded_hdg_label.grid(row=8, column=0, columnspan=4, pady=(5, 0), sticky="w")
        
        self.ded_hdg: tk.StringVar = tk.StringVar()
        self.ded_hdg_spin: tk.Spinbox = tk.Spinbox(self.frame, from_=0, to=359, increment=1, textvariable=self.ded_hdg, fg="black", bg="white")
        self.ded_hdg_spin.configure(width=12)
        self.ded_hdg_spin.grid(row=8, column=4, columnspan=4, sticky="w", pady=(3,0))
    
    def clear_panel(self) -> None:
        self.fno_entry.delete(0, tk.END)
        
        self.hdg.set(0)
        self.alt.set(3000)
        self.spd.set(180)
        
        self.wayp_menu.set(self.waypoints[0])
        if not self.landing.get():
            self.landing.set(value=True)
            self.toggle_landing()
        self.rno_menu.set("09 L")
    
    def draw_clr_btn(self) -> None:
        self.clr_btn: tk.Button = tk.Button(self.frame, text="CLEAR ALL", bg="#828783", font=("", 7, "bold"), command=self.clear_panel)
        self.clr_btn.configure(width=32, height=1 )
        self.clr_btn.grid(row=11, column=0, columnspan=7, sticky="w", pady=(5,0))
        
    def draw_add_flight_btn(self) -> None:
        def entry_check() -> None:
            if FlightPath.count_traffic() == 10:
                self.logger.log("Airspace Full")
                return
            
            match EntryCheck.check_all_data(self):
                case 1:
                    entry_hdg = WaypointUtils.get_entry_heading(int(self.hdg.get()), WaypointUtils.get_waypoint_coords(self.wayp_menu.get()))
                    entry_coords = WaypointUtils.get_entry_coords(155, entry_hdg)

                    if self.landing.get():
                        fl_path = OptimumPath.optimal_flight_path(str(self.wayp_menu.get()), (True, self.rno_menu.get()))
                        fl_path += f'~{entry_coords}'
                    else:
                        fl_path = OptimumPath.optimal_flight_path(str(self.wayp_menu.get()), (False, int(self.ded_hdg.get())))
                    
                    def deter_rate(spd: int) -> str:
                        if spd > 185:
                            return "Fast"
                        elif spd > 175:
                            return "Steady"
                        else:
                            return "Slow"
                    
                    wp_ords = WaypointUtils.get_waypoint_coords(self.wayp_menu.get())
                    entry_hdg = WaypointUtils.get_entry_heading(int(self.hdg.get()), wp_ords)
                    dist_from_wp = round(WaypointUtils.convert_scale(px=WaypointUtils.dist_betw_two_coords(wp_ords, entry_coords)), 2)
                    
                    FM_Data.add_flight_data(self.fno_entry.get(), int(self.hdg.get()), f"{(int(entry_coords[0]),int(entry_coords[1]))}", int(self.alt.get()), int(self.spd.get()), 0)
                    FlightPath.add_flight_path(self.fno_entry.get(), fl_path, dist_from_wp, deter_rate(int(self.spd.get())))
                    
                    miles = WaypointUtils.track_miles(self.fno_entry.get())
                    if "(0, 0)" in fl_path.split("~"):
                        climb_gradient = -abs(1200 - int(self.alt.get())) / (miles-12.5)
                    else:
                        climb_gradient = (4650 - int(self.alt.get())) / (miles+5)
                    
                    FM_Data.climb_rate(self.fno_entry.get(), climb_gradient)
                    
                    if Radar.hover_fno == "hover_plane":
                        Radar.hover_fno = self.fno_entry.get()
                    
                    self.logger.log(f"Flight {self.fno_entry.get()} entering airspace.")
                    self.clear_panel()
                case -1:
                    self.logger.log("Invalid Flight Code.", "red")
                case -8:
                    self.logger.log("Flight already exists in Radar.", "red")
                case -2:
                    self.logger.log("Invalid Heading.", "red")
                case -3:
                    self.logger.log("Invalid Altitude.", "red")
                case -4:
                    self.logger.log("Invalid Airspeed.", "red")
                case -5:
                    self.logger.log("Invalid Waypoint.", "red")
                case -6:
                    self.logger.log("Invalid Route Heading.", "red")
                case -7:
                    self.logger.log("Other Aircrafts in close proximity", "red")
                case -9:
                    self.logger.log("Waypoint too Busy", "red")
            
        self.add_fl_btn: tk.Button = tk.Button(self.frame, text="ADD FLIGHT", bg="#828783", font=("", 7, "bold"), command=entry_check)
        self.add_fl_btn.configure(width=32, height=1)
        self.add_fl_btn.grid(row=10, column=0, columnspan=7, sticky="w" , pady=(15,0))
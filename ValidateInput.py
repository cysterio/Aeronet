import re
import math
from Utils.Logic.WaypointUtils import WaypointUtils
from Utils.Update.FM_DataUtils import FM_Data
from Utils.Update.FlightPathUtils import FlightPath

class EntryCheck:
    @staticmethod
    def check_all_data(data: object) -> int:
        if not EntryCheck.is_valid_fno(data.fno_entry.get()):
            return -1
        if not EntryCheck.is_duplicate_fno(data.fno_entry.get()):
            return -8
        if not EntryCheck.is_valid_heading(data.hdg.get()):
            return -2
        if not EntryCheck.is_valid_altitude(data.alt.get(), data.landing.get()):
            return -3
        if not EntryCheck.is_valid_airspeed(data.spd.get()):
            return -4
        if not EntryCheck.is_valid_waypoint(int(data.hdg.get()), data.wayp_menu.get()):
            return -5
        if not data.landing.get():
            entry_hdg = WaypointUtils.get_entry_heading(int(data.hdg.get()), WaypointUtils.get_waypoint_coords(data.wayp_menu.get()))
            if not EntryCheck.is_valid_ded_hdg(int(data.ded_hdg.get()), entry_hdg):
                return -6
        if not EntryCheck.check_proximity(data.wayp_menu.get(), int(data.hdg.get()), int(data.alt.get())):
            return -7
        if not EntryCheck.check_waypoint(data.wayp_menu.get()):
            return -9
        return 1

    @staticmethod
    def is_valid_fno(fno: str) -> bool:
        r_exp = r"^(?=.{2,7}$)[A-Z]{1,3}[0-9]{1,4}[A-Z]{0,1}$"
        return re.match(r_exp, fno) is not None
    
    @staticmethod
    def is_duplicate_fno(fno: str) -> bool:
        return fno not in FM_Data.get_all_fno()

    @staticmethod
    def is_valid_heading(hdg: str) -> bool:
        try:
            return int(hdg) in range(360)
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_airspeed(spd: str) -> bool:
        try:
            return int(spd) in range(150, 201)
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_altitude(alt: str, landing: bool) -> bool:
        try:
            if not landing:
                return int(alt) in range(3500, 5001)
            else:
                return int(alt) in range(2500, 4001)
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_waypoint(hdg: int, wp: str) -> bool:
        x, y = WaypointUtils.get_waypoint_coords(wp)
        theta = WaypointUtils.to_positive_theta(math.degrees(math.atan2(y, x)))
        
        lim = []
        
        for i in [theta + 15, theta - 15]:
            angle = math.degrees(math.atan2((155 * math.sin(math.radians(i))) - y, (155 * math.cos(math.radians(i))) - x)) + 180
            lim.append(WaypointUtils.azimuth_to_heading(int(round(WaypointUtils.to_positive_theta(angle)))))
        
        if lim[1] >= lim[0]:
            return hdg in range(lim[0], lim[1] + 1)
        else:
            return hdg in range(lim[0], 360) or hdg in range(0, lim[1] + 1)
    
    @staticmethod
    def is_valid_ded_hdg(ded_hdg: int, ent_hdg: int) -> bool:
        try:
            return ded_hdg in range(360) and ded_hdg not in range((ent_hdg - 75), (ent_hdg + 76))
        except ValueError:
            return False
    
    @staticmethod
    def check_proximity(way_p: str, hdg: int, alt: int) -> bool:
        radar_radius = 155
        entry_hdg = WaypointUtils.get_entry_heading(hdg, WaypointUtils.get_waypoint_coords(way_p))
        
        entry_coords = WaypointUtils.get_entry_coords(radar_radius, entry_hdg)
        curr_coords = FM_Data.get_current_coords()
        
        proxi_crafts: list[tuple[str, tuple[float, float]]] = []
        
        for i in curr_coords:
            tupord = tuple(i)
            dist = WaypointUtils.dist_betw_two_coords(entry_coords, tupord[1])
            
            if dist < 5: 
                proxi_crafts.append(tupord)
        
        proxy_fl_no = [i[0] for i in proxi_crafts]
        if len(proxy_fl_no) > 0:
            curr_alt = FM_Data.get_proxy_altitudes(proxy_fl_no)
        else:
            curr_alt = []
        
        for i in curr_alt:
            if abs(alt - i) < 305:
                return False
        
        return True
    
    @staticmethod
    def check_waypoint(way_p: str) -> bool:
        fnos = FM_Data.get_all_fno()
        
        cnt = 0
        for fcode in fnos:
            waypoints = FlightPath.waypoints(fcode).split("~")
            if waypoints[0] == way_p:
                cnt += 1
                
                if cnt == 2:
                    return False
        return True
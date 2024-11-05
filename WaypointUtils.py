import os
import json
import math

from Utils.Update.FlightPathUtils import FlightPath
from Utils.Update.FM_DataUtils import FM_Data

class WaypointUtils:
    @staticmethod
    def fetch_waypoints() -> dict:
        waypoints_path = os.path.join(os.path.dirname(__file__), "Waypoints.json")
        with open(waypoints_path, "r") as file:
            json_file = json.loads(file.read())
            return dict(json_file)

    @staticmethod
    def get_waypoint_coords(waypoint_name: str) -> tuple[float, float]:
        waypoints = WaypointUtils.fetch_waypoints()
        
        for waypoint_type in ["Primary", "Secondary", "Tertiary"]:
            if waypoint_name in waypoints[waypoint_type]:
                return eval(waypoints[waypoint_type][waypoint_name])
        
        return tuple(eval(waypoint_name))

    @staticmethod
    def dist_betw_two_coords(coords_1: tuple[float, float], coords_2: tuple[float, float]) -> float:
        exp = (coords_1[0] - coords_2[0])**2 + (coords_1[1] - coords_2[1])**2
        return math.sqrt(exp)

    @staticmethod
    def convert_scale(px: float = -1, nm: float = -1) -> float:
        if px == -1:
            return nm * 155 / 30
        elif nm == -1:
            return px * 30 / 155

    @staticmethod
    def dist_from_waypoint(pl: tuple[float, float], wp: str) -> float:
        x1, y1 = pl
        x2, y2 = WaypointUtils.get_waypoint_coords(wp)
        
        return math.sqrt(WaypointUtils.convert_scale(px=x2 - x1)**2 + 
                         WaypointUtils.convert_scale(px=y2 - y1)**2)

    @staticmethod
    def dist_betw_waypoints(w1: str, w2: str) -> float:
        x1, y1 = WaypointUtils.get_waypoint_coords(w1)
        x2, y2 = WaypointUtils.get_waypoint_coords(w2)
        
        return math.sqrt(WaypointUtils.convert_scale(px=x2 - x1)**2 + 
                         WaypointUtils.convert_scale(px=y2 - y1)**2)

    @staticmethod
    def get_entry_coords(radar_radius: float, entry_hdg: float) -> tuple[float, float]:
        entry_azm = WaypointUtils.heading_to_azimuth(entry_hdg)
        return (radar_radius * math.cos(math.radians(entry_azm)), 
                radar_radius * math.sin(math.radians(entry_azm)))

    @staticmethod
    def track_miles(fno: str) -> float:
        flight_path = FlightPath.waypoints(fno)
        waypoints = flight_path.split('~')
        
        curr_coords = FM_Data.coordinates(fno)
        wp1 = WaypointUtils.get_waypoint_coords(waypoints[0])
        
        dst = WaypointUtils.dist_betw_two_coords(curr_coords, wp1)
        miles = WaypointUtils.convert_scale(px=dst)

        if "(0, 0)" in waypoints:
            waypoints = waypoints[0:waypoints.index("(0, 0)") + 1]

        for i in range(len(waypoints) - 1):
            miles += WaypointUtils.dist_betw_waypoints(waypoints[i], waypoints[i + 1])
        
        return miles

    @staticmethod
    def to_positive_theta(theta: float) -> float:
        if theta < 0:
            return 360 + theta
        elif theta <= 359.9:
            return theta
        else:
            return theta % 360

    @staticmethod
    def azimuth_to_heading(hdg: float) -> float:
        if 90 - hdg >= 0:
            return 90 - hdg
        else:
            return 450 - hdg

    @staticmethod
    def heading_to_azimuth(theta: float) -> float:
        if 90 - theta >= 0:
            return 90 - theta
        else:
            return 450 - theta

    @staticmethod
    def get_entry_heading(hdg: float, wp: tuple[float, float]) -> float:
        r = 155
        x, y = wp
        azm = WaypointUtils.heading_to_azimuth(WaypointUtils.to_positive_theta(hdg + 180))
        m = math.tan(math.radians(azm))
        
        a = 1 + m**2
        b = -2 * m * (m * x - y)
        c = (m * x - y)**2 - r**2

        discriminant = b**2 - 4 * a * c

        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        y1 = m * (x1 - x) + y
        y2 = m * (x2 - x) + y
        
        def theta_to_azimuth(theta: float, y: float) -> float:
            if y >= 0:
                return theta
            else:
                return 360 - theta
        
        if abs(x1) <= 156 and abs(y1) <= 156:
            deg1 = round(math.degrees(math.atan2(y1, x1)))
        elif abs(x1) <= 156:
            deg1 = theta_to_azimuth(round(math.degrees(math.acos(x1 / 155))), y1)
        elif abs(y1) <= 156:
            deg1 = theta_to_azimuth(round(math.degrees(math.asin(y1 / 155))), y1)
            
        if abs(x2) <= 156 and abs(y2) <= 156:
            deg2 = round(math.degrees(math.atan2(y2, x2)))
        elif abs(x2) <= 156:
            deg2 = theta_to_azimuth(round(math.degrees(math.acos(x2 / 155))), y2)
        elif abs(y2) <= 156:
            deg2 = theta_to_azimuth(round(math.degrees(math.asin(y2 / 155))), y2)
        
        deg1 = WaypointUtils.azimuth_to_heading(deg1)
        deg2 = WaypointUtils.azimuth_to_heading(deg2)
        
        theta = round(WaypointUtils.azimuth_to_heading(WaypointUtils.to_positive_theta(math.degrees(math.atan2(y, x)))))
        lim = [WaypointUtils.to_positive_theta(theta - 15), WaypointUtils.to_positive_theta(theta + 15)]
        
        if lim[1] >= lim[0]:
            if deg1 in range(lim[0], lim[1] + 1):
                return deg1
            elif deg2 in range(lim[0], lim[1] + 1):
                return deg2
        else:
            if deg1 in range(lim[0], 360) or deg1 in range(0, lim[1] + 1):
                return deg1
            elif deg2 in range(lim[0], 360) or deg2 in range(0, lim[1] + 1):
                return deg2

    @staticmethod
    def find_nxt_heading(i_coords: tuple[float, float], f_coords: tuple[float, float]) -> int:
        x1, y1 = i_coords
        x2, y2 = f_coords

        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        
        return int(WaypointUtils.azimuth_to_heading(angle))
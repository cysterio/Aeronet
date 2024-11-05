from Utils.Logic.WaypointUtils import WaypointUtils
from Utils.Update.FM_DataUtils import FM_Data
from Utils.Update.FlightPathUtils import FlightPath

import math

class AnimateUtils:
    @staticmethod
    def get_coord_step(fno: int, i_coords: tuple[float, float]) -> tuple[float, float]:
        path: str = FlightPath.waypoints(fno).split("~")
        wp_coords: tuple[float, float] = WaypointUtils.get_waypoint_coords(path[0])
        
        time: float = AnimateUtils.time_to_reach_wp(fno)
        time = 1e-30 if time == 0 else time 
        
        if time > 10000:
            return (0.0, 0.0)
        
        x_step: float = 3 * (wp_coords[0] - i_coords[0]) / time
        y_step: float = 3 * (wp_coords[1] - i_coords[1]) / time
        
        return (x_step, y_step)
    
    @staticmethod
    def get_altitude_step(fno: int, i_coords: tuple[float, float], alt: float) -> float:
        dst: float = WaypointUtils.dist_betw_two_coords(FM_Data.coordinates(fno), i_coords)
        step_mile: float = WaypointUtils.convert_scale(px=dst)
        
        path: str = FlightPath.waypoints(fno)
        miles: float = WaypointUtils.track_miles(fno)
        landing: bool = "(0, 0)" in path.split("~")
        
        if landing:
            if miles < 12:
                climb_rate: float = -alt / miles
                FM_Data.climb_rate(fno, climb_rate)
            else:
                climb_rate: float = FM_Data.climb_rate(fno)
                if alt < 1180 and climb_rate != 0:
                    FM_Data.climb_rate(fno, 0)
        
        if not landing and alt > 4650:
            FM_Data.climb_rate(fno, 0)
        
        climb_rate: float = FM_Data.climb_rate(fno)
        return climb_rate * step_mile
    
    @staticmethod
    def determine_speed(fno: int) -> int:
        rate: str = FlightPath.rate_assign(fno)
        path: str = FlightPath.waypoints(fno)
        landing: bool = "(0, 0)" in path.split("~")
        speed: list[int] = [150, 180, 200]
        
        miles: float = WaypointUtils.track_miles(fno)
        
        if landing:
            if miles < 25:
                speed = [130, 150, 170]
            if miles < 15:
                speed = [115, 130, 150]
            if miles < 5:
                speed = [115, 120, 130]
        
        match rate:
            case "Slow":
                return speed[0]
            case "Steady":
                return speed[1]
            case "Fast":
                return speed[2]
            case "Landing":
                return 0
    
    @staticmethod
    def get_airspeed_step(fno: int, spd: float) -> float:
        target_spd: int = AnimateUtils.determine_speed(fno)
        
        if target_spd == 0:
            return float(target_spd)
        
        diff: float = target_spd - spd
        return 2 * diff / abs(diff) if abs(diff) > 2 else diff
    
    @staticmethod
    def time_to_reach_wp(fno: int) -> float:
        dst: float = FlightPath.dist_from_waypoint(fno)
        spd: float = FM_Data.air_speed(fno)
        
        spd = 1e-30 if spd == 0 else spd
        return (dst / spd) * 3600

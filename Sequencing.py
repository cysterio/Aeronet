from datetime import datetime, timedelta
from Interface.Panels.Radar import Radar

from Utils.Logic.WaypointUtils import WaypointUtils
from Utils.Update.FM_DataUtils import FM_Data
from Utils.Update.FlightPathUtils import FlightPath
from Utils.Update.ScheduleUtils import Schedule

class Sequencing:
    landing_fno: list = []
    take_off_fno: list = []
    
    rwy_available: bool | int = True
    
    @staticmethod
    def land_aircraft(fcode: str) -> None:
        Sequencing.landing_fno.append(fcode)
        
        FM_Data.altitude(fcode, 0)
        FM_Data.air_speed(fcode, 0)
        FM_Data.heading(fcode, 0)
        FM_Data.coordinates(fcode, (0,0))
        FM_Data.climb_rate(fcode, 0)
        
        path: list = FlightPath.waypoints(fcode).split("~")
        FlightPath.waypoints(fcode, "~".join(path[1:]))
        
        Sequencing.rwy_available = -15
        
        arr_time: datetime = datetime.now()
        dep_time: datetime = arr_time + timedelta(seconds=10)
        Schedule.add_flight(fcode, str(dep_time)[0:19])
    
    @staticmethod
    def take_off_aircraft(fcode: str) -> None:
        Sequencing.take_off_fno.remove(fcode)
        
        path: list = FlightPath.waypoints(fcode).split("~")
        f_wayp_coords: tuple = WaypointUtils.get_waypoint_coords(path[0])
        
        Sequencing.rwy_available = -25
        
        FM_Data.altitude(fcode, 18)
        FM_Data.air_speed(fcode, 120)
        FlightPath.rate_assign(fcode, "Steady")
        FM_Data.coordinates(fcode, (0,3 * (f_wayp_coords[1] / abs(f_wayp_coords[1]))))
        FM_Data.heading(fcode, WaypointUtils.find_nxt_heading((0,0), f_wayp_coords))
        FM_Data.climb_rate(fcode, 95)
        
        if Radar.hover_fno == "hover_plane":
            Radar.hover_fno = fcode
    
    @staticmethod
    def check_landing_traffic(fno: str) -> bool:
            fnos: list = FM_Data.get_all_fno()
            fno_path: str = FlightPath.waypoints(fno)
            
            for fcode in fnos:
                if fno == fcode:
                    continue
                
                path: list = FlightPath.waypoints(fcode).split("~")
                alt: float = FM_Data.altitude(fcode)
                landing: bool = "(0, 0)" in path
                
                if not landing or alt > 3000:
                    continue
                
                if path[0] == fno_path[0] or path[0] == "(0, 0)":
                    p_coords: tuple = FM_Data.coordinates(fcode)
                    dst: float = WaypointUtils.dist_from_waypoint(p_coords, path[0])
                    
                    if dst < 9:
                        return False
            return True

    @staticmethod
    def fix_landing_collisions() -> None:
        flight_data: dict = {
            "FENRO": {"flights": {}, "waypoints": [("ARVEX", "BORAX"), ("ELMOS", "CALMA")]},
            "DUNES": {"flights": {}, "waypoints": [("HOMER", "GAMMA"), ("ELMOS", "CALMA")]}
        }

        for fno in FM_Data.get_all_fno():
            path: list = FlightPath.waypoints(fno).split("~")
            if "(0, 0)" not in path or path[0] not in flight_data:
                continue
            
            if not path[1] == "(0, 0)":
                continue 
            
            start_point: str = path[0]
            coords: tuple = FM_Data.coordinates(fno)
            flight_data[start_point]["flights"][fno] = WaypointUtils.dist_from_waypoint(coords, start_point)

        for start_point, data in flight_data.items():
            sorted_flights: list = sorted(data["flights"].items(), key=lambda x: x[1])
            if len(sorted_flights) > 3:
                dsts: dict = {}

                for fno1, dist1 in sorted_flights:
                    for fno2, dist2 in data["flights"].items():
                        if fno1 == fno2 or (f"{fno2}~{fno1}" in dsts):
                            continue
                        dsts[f"{fno1}~{fno2}"] = abs(dist1-dist2)
                
                min_dist: float = min(list(dsts.values()))

                for fnos, dist in dsts.items():
                    if dist == min_dist:
                        fno1: str
                        fno2: str
                        fno1, fno2 = tuple(fnos.split("~"))
                        flt_no: str = fno1 if data["flights"][fno1] < data["flights"][fno2] else fno2
                        index: int = next((i for i, tup in enumerate(sorted_flights) if tup[0] == flt_no), None)
                        sorted_flights.append(sorted_flights.pop(index)) 
            
            if start_point in ["FENRO", "DUNES"]:
                rates: list = ["Fast", "Steady", "Slow"]
                for flight, rate in zip([f[0] for f in sorted_flights[:3]], rates):
                    FlightPath.rate_assign(flight, rate)
            
            if len(sorted_flights) <= 3:
                return
            
            for flight, _ in sorted_flights[3:]:
                coords: tuple = FM_Data.coordinates(flight)
                wp1: str
                wp2: str
                wp1, wp2 = data["waypoints"][0]
                mid_wp: str
                end_wp: str
                mid_wp, end_wp = data["waypoints"][1]
                
                new_path: str
                if WaypointUtils.dist_from_waypoint(coords, wp1) > WaypointUtils.dist_from_waypoint(coords, wp2):
                    new_path = f"{start_point}~{mid_wp}~{wp1}~{start_point}~(0, 0)"
                elif WaypointUtils.dist_from_waypoint(coords, wp1) < WaypointUtils.dist_from_waypoint(coords, wp2):
                    new_path = f"{start_point}~{end_wp}~{wp2}~{start_point}~(0, 0)"
                else:
                    new_path = f"{start_point}~{end_wp}~{wp2}~{start_point}~(0, 0)" if start_point == "FENRO" else f"{start_point}~{mid_wp}~{wp1}~{start_point}~(0, 0)"

                FlightPath.waypoints(flight, new_path)
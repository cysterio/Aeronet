from Interface.Blocs.AnimateUtils import AnimateUtils
from Utils.Logic.WaypointUtils import WaypointUtils
from Utils.Update.FlightPathUtils import FlightPath
from Utils.Update.FM_DataUtils import FM_Data

import heapq
import numpy as np

class AntiCollision:
    offtime: int = 60
    
    @staticmethod
    def lines_intersect(line1: tuple, line2: tuple) -> tuple:
        x1: float
        y1: float
        x2: float
        y2: float
        x1, y1, x2, y2 = line1
        x3: float
        y3: float
        x4: float
        y4: float
        x3, y3, x4, y4 = line2

        det: float = (x4 - x3) * (y2 - y1) - (y4 - y3) * (x2 - x1)

        if det == 0:
            points: list = []
            
            if line1 == line2 or line1 == line2[2:] + line2[:2]:
                    step_x: float = (x2 - x1) / 7
                    step_y: float = (y2 - y1) / 7

                    i: np.ndarray = np.arange(1, 7)
                    new_x: np.ndarray = x1 + i * step_x
                    new_y: np.ndarray = y1 + i * step_y

                    points = list(zip(new_x, new_y))
            return (points, -1)

        t1: float = ((x4 - x3) * (y3 - y1) - (y4 - y3) * (x3 - x1)) / det
        t2: float = ((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)) / det

        if (t1 >= 0 and t1 <= 1) and (t2 >= 0 and t2 <= 1):
            return (x1 + t1*(x2-x1), y3 + t2*(y4-y3))
        return (False,)

    @staticmethod
    def get_poi_alt_and_time(fno: str, poi: tuple, wp: str | tuple, grad: bool | float = False, airspeed: bool | float = False) -> tuple:
        alt: float = FM_Data.altitude(fno)
        rate_assign: float
        if airspeed == False:
            rate_assign = AnimateUtils.determine_speed(fno)
        else:
            rate_assign = airspeed
        coords: tuple = FM_Data.coordinates(fno)
        climb_grad: float
        if grad == False:
            climb_grad = FM_Data.climb_rate(fno)
        else:
            climb_grad = grad

        if isinstance(wp, str):
            wp = WaypointUtils.get_waypoint_coords(wp)
        
        dst: float = WaypointUtils.convert_scale(px=WaypointUtils.dist_betw_two_coords(coords,wp) + WaypointUtils.dist_betw_two_coords(poi,wp))
        return ((dst * climb_grad) + alt, dst/rate_assign * 3600)

    @staticmethod
    def get_line(fno: str) -> tuple | None:
        nxt: str = FlightPath.waypoints(fno)
        wps: list = nxt.split("~")
        if "(0, 0)" not in wps[:2] and len(wps) >= 2:
            x1: float
            y1: float
            x1, y1 = WaypointUtils.get_waypoint_coords(wps[0])
            x2: float
            y2: float
            x2, y2 = WaypointUtils.get_waypoint_coords(wps[1])

            return (x1, y1, x2, y2)
        return None

    @staticmethod
    def conflict_possibilities() -> dict:    
        conflict_possibilities: dict = {}
        fnos: list = FM_Data.get_all_fno()

        for i in fnos:
            line1: tuple | None = AntiCollision.get_line(i)
            if not line1:
                continue
            
            for j in fnos:
                if i == j:
                    continue
                
                line2: tuple | None = AntiCollision.get_line(j)
                if not line2:
                    continue
                
                intersect: tuple = AntiCollision.lines_intersect(line1, line2)
                if intersect[0] == False:
                    continue

                c_fnos: str = f'{i}~{j}'

                if not intersect[1] == -1:
                    a1: float
                    t1: float
                    a1, t1 = AntiCollision.get_poi_alt_and_time(i, intersect, AntiCollision.get_line(i)[:2])
                    a2: float
                    t2: float
                    a2, t2 = AntiCollision.get_poi_alt_and_time(j, intersect, AntiCollision.get_line(j)[:2])
                    
                    if abs(t1 - t2) < AntiCollision.offtime and abs(a1 - a2) < 300:
                        if c_fnos not in conflict_possibilities:
                            if "~".join(c_fnos.split("~")[::-1]) not in conflict_possibilities:
                                conflict_possibilities[c_fnos] = intersect

                else:
                    x3: float
                    y3: float
                    x3, y3 = WaypointUtils.get_waypoint_coords(FlightPath.waypoints(i).split("~")[0])
                    x4: float
                    y4: float
                    x4, y4 = WaypointUtils.get_waypoint_coords(FlightPath.waypoints(j).split("~")[0])

                    possible: list = []
                    for x1, y1 in intersect[0]:
                        a1: float
                        t1: float
                        a1, t1 = AntiCollision.get_poi_alt_and_time(i, (x1, y1), (x3, y3))
                        a2: float
                        t2: float
                        a2, t2 = AntiCollision.get_poi_alt_and_time(j, (x1, y1), (x4, y4))
                        alt1: float = abs(a1 - a2)
                        
                        if abs(t1 - t2) < AntiCollision.offtime and alt1 < 300:
                            heapq.heappush(possible, (alt1, (x1, y1)))

                    if not possible:
                        continue

                    intersect_pt: tuple = heapq.heappop(possible)[1]

                    if c_fnos not in conflict_possibilities and "~".join(c_fnos.split("~")[::-1]) not in conflict_possibilities:
                        conflict_possibilities[c_fnos] = intersect_pt
                        
        return conflict_possibilities

    @staticmethod
    def fix_conflict(conflict_possibilities: dict) -> None:
        for conflict_p in conflict_possibilities:
            fno1: str = conflict_p.split("~")[0]
            fno2: str = conflict_p.split("~")[1]

            p1: list = FlightPath.waypoints(fno1).split("~")
            p2: list = FlightPath.waypoints(fno2).split("~")

            landing1: bool = "(0, 0)" in p1
            landing2: bool = "(0, 0)" in p2

            poi: tuple = conflict_possibilities[conflict_p]

            poi_alt1: float
            poi_time1: float
            poi_alt1, poi_time1 = AntiCollision.get_poi_alt_and_time(fno1, poi, p1[0])

            poi_alt2: float
            poi_time2: float
            poi_alt2, poi_time2 = AntiCollision.get_poi_alt_and_time(fno2, poi, p2[0])

            def alter_rate_assign(fno1: str, fno2: str, poi: tuple, rate: str | None) -> bool:
                rate_assign: str = FlightPath.rate_assign(fno1)
                rates: list = ["Slow", "Steady", "Fast"]
                
                if rate:
                    rate_range: list = list(range(rates.index(rate_assign), 3))
                else:
                    rate_range: list = list(range(rates.index(rate_assign), -1, -1))
                    
                nxt_wp1: str = FlightPath.waypoints(fno1).split("~")[0]
                nxt_wp2: str = FlightPath.waypoints(fno2).split("~")[0]
                
                poi_time2: float = AntiCollision.get_poi_alt_and_time(fno2, poi, nxt_wp2)[1]
                
                for i in rate_range:
                    FlightPath.rate_assign(fno1, rates[i])
                    speed: float = AnimateUtils.determine_speed(fno1)
                    
                    poi_time1: float = AntiCollision.get_poi_alt_and_time(fno1, poi, nxt_wp1, airspeed=speed)[1]
                    
                    if abs(poi_time1 - poi_time2) < AntiCollision.offtime:
                        return False
                return True

            def alter_climb_gradient(fno1: str, fno2: str, poi: tuple, grad: bool) -> bool:
                climb_grad: float = FM_Data.climb_rate(fno1)
                if grad:
                    grad_range: list = list(range(climb_grad, 121, 5))
                else:
                    grad_range: list = list(range(climb_grad, 60, -5))
                
                nxt_wp1: str = FlightPath.waypoints(fno1).split("~")[0]
                nxt_wp2: str = FlightPath.waypoints(fno2).split("~")[0]
                
                poi_alt2: float = AntiCollision.get_poi_alt_and_time(fno2, poi, nxt_wp2)[0]
                
                for i in grad_range:
                    FM_Data.climb_rate(fno1, i)
                    poi_alt1: float = AntiCollision.get_poi_alt_and_time(fno1, poi, nxt_wp1)[0]
                    
                    if abs(poi_alt1 - poi_alt2) > 300:
                        return False
                
                return True

            def try_actions(*actions: list) -> None:
                for action in actions:
                    if not action():
                        return

            if landing1 and landing2:
                if poi_time1 > poi_time2:
                    try_actions(
                        lambda: alter_rate_assign(fno2, fno1, poi, True),
                        lambda: alter_rate_assign(fno1, fno2, poi, False)
                    )
                else:
                    try_actions(
                        lambda: alter_rate_assign(fno1, fno2, poi, True),
                        lambda: alter_rate_assign(fno2, fno1, poi, False)
                    )

            elif landing1 and not landing2:
                try_actions(
                    lambda: alter_climb_gradient(fno2, fno1, poi, poi_alt1 < poi_alt2),
                    lambda: alter_rate_assign(fno2, fno1, poi, poi_time1 >= poi_time2),
                    lambda: alter_rate_assign(fno1, fno2, poi, poi_time1 < poi_time2)
                )

            elif not landing1 and landing2:
                try_actions(
                    lambda: alter_climb_gradient(fno1, fno2, poi, poi_alt2 < poi_alt1),
                    lambda: alter_rate_assign(fno1, fno2, poi, poi_time1 > poi_time2),
                    lambda: alter_rate_assign(fno2, fno1, poi, poi_time1 <= poi_time2)
                )

            else:
                try_actions(
                    lambda: alter_climb_gradient(fno2, fno1, poi, poi_alt1 < poi_alt2),
                    lambda: alter_climb_gradient(fno1, fno2, poi, poi_alt1 >= poi_alt2),
                    lambda: alter_rate_assign(fno2, fno1, poi, poi_time1 < poi_time2),
                    lambda: alter_rate_assign(fno1, fno2, poi, poi_time1 >= poi_time2)
                )

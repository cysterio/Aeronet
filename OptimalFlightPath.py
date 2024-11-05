import math
from Utils.Logic.WaypointUtils import WaypointUtils

class OptimumPath:
    @staticmethod
    def optimal_flight_path(entry_wp: str, landing_details: tuple[bool, float]) -> str:
        WAYPOINTS: dict[str, dict[str, tuple[float, float]]] = WaypointUtils.fetch_waypoints()

        for key in ["Primary", "Secondary", "Tertiary"]:
            for i, j in WAYPOINTS[key].items():
                WAYPOINTS[key][i] = eval(j)

        WP_BOUND: dict[str, str] = {'LAMOR': 'ARVEX', 'VEVAK': 'BORAX', 'ROCKY': 'GAMMA', 'PAGAN': 'HOMER'}
        QUAD_TRANS_LOGIC: dict[str, list[str]] = {
            'CALMA': ['+-++', '+++-'],
            'ELMOS': ['-+--', '---+'],
            'HOMER~GAMMA': ['--+-'],
            'GAMMA~HOMER': ['+---'],
            'BORAX~ARVEX': ['++-+'],
            'ARVEX~BORAX': ['-+++']
        }
        DOUBLE_TRANS_LOGIC: dict[str, list[tuple[str]]] = {
            '++--': [('CALMA~DUNES'), ('FENRO~ELMOS')],
            '--++': [('DUNES~CALMA'), ('ELMOS~FENRO')],
            '-++-': [('FENRO~CALMA'), ('ELMOS~DUNES')],
            '+--+': [('CALMA~FENRO'), ('DUNES~ELMOS')]
        }
        ON_AXIS_TRANS_LOGIC: dict[tuple[str], list[str]] = {
            ('FENRO~CALMA',): ['- + '],
            ('DUNES~ELMOS',): ['+ - '],
            ('BORAX',): [' ++ ', '+  +'],
            ('ARVEX',): ['-  +', ' +- '],
            ('HOMER',): ['-  -', ' -- '],
            ('GAMMA',): ['+  -', ' -+ ']
        }
        ON_AXIS_NZ_TRANS_LOGIC: dict[str, tuple[str, str]] = {
            'KENVA': ('ARVEX~ELMOS', 'BORAX~CALMA'),
            'NELTS': ('ELMOS~FENRO', 'ELMOS~DUNES'),
            'TANGO': ('CALMA~DUNES', 'CALMA~FENRO'),
            'QUEST': ('HOMER~ELMOS', 'GAMMA~CALMA')
        }
        LANDING_LOGIC: dict[str | int, tuple[str, str]] = {
            'KENVA': ('FENRO', 'ARVEX~ELMOS~HOMER~DUNES'),
            'QUEST': ('GAMMA~CALMA~BORAX~FENRO', 'DUNES'),
            'TANGO': ('BORAX~FENRO', 'GAMMA~DUNES'),
            'NELTS': ('ARVEX~FENRO', 'HOMER~DUNES'),
            1: ('BORAX~FENRO', 'CALMA~GAMMA~DUNES'),
            2: ('ARVEX~FENRO', 'ELMOS~HOMER~DUNES'),
            3: ('HOMER~DUNES', 'ELMOS~ARVEX~FENRO'),
            4: ('GAMMA~DUNES', 'CALMA~BORAX~FENRO')
        }
        QUAD_BOUND: dict[str, list[str]] = {'KENVA~QUEST': ['ARVEX~ELMOS~HOMER'], 'QUEST~KENVA': ['GAMMA~CALMA~BORAX']}

        def determine_quadrant(x: float, y: float) -> int:
            if x > 0 and y > 0:
                return 1
            elif x < 0 and y > 0:
                return 2
            elif x < 0 and y < 0:
                return 3
            elif x > 0 and y < 0:
                return 4
            else:
                return -10

        def heading_to_azimuth(theta: float) -> float:
            return 90 - theta if 90 - theta >= 0 else 450 - theta

        def get_entry_point_coords(theta: float, r: float = 150) -> tuple[float, float]:
            return (r * math.cos (math.radians(theta)), r * math.sin(math.radians(theta)))

        def exit_wp(heading: float) -> str:
            entry_coords: tuple[float, float] = get_entry_point_coords(heading_to_azimuth(heading))
            wp_dists: dict[str, float] = {wp_name: WaypointUtils.dist_betw_two_coords(WAYPOINTS['Primary'][wp_name], entry_coords) for wp_name in WAYPOINTS['Primary']}
            min_dist: float = min(list(wp_dists.values()))
            for wp, dist in wp_dists.items():
                if dist == min_dist:
                    return (WP_BOUND[wp] + '~' + wp) if wp in WP_BOUND else wp

        def sign_manager(entry_wp: str, exit: str) -> str:
            return ''.join('+' if i > 0 else '-' if i < 0 else ' ' for i in [*WaypointUtils.get_waypoint_coords(entry_wp), *WaypointUtils.get_waypoint_coords(exit.split("~")[-1])])

        def quad_transition_nznv(entry_wp: str, exit: str) -> str:
            signs: str = sign_manager(entry_wp, exit)
            for wp in QUAD_TRANS_LOGIC:
                if signs in QUAD_TRANS_LOGIC[wp]:
                    return wp

        def quad_transition_nzv(entry_wp: str, exit: str) -> str:
            x: str = DOUBLE_TRANS_LOGIC[sign_manager(entry_wp, exit)][0]
            y: str = DOUBLE_TRANS_LOGIC[sign_manager(entry_wp, exit)][1]
            e: tuple[float, float] = WaypointUtils.get_waypoint_coords(entry_wp)
            if (WaypointUtils.dist_betw_two_coords(WaypointUtils.get_waypoint_coords(x.split("~")[0]), e)) <= (WaypointUtils.dist_betw_two_coords(WaypointUtils.get_waypoint_coords(y.split("~")[0]), e)):
                return x
            else:
                return y

        def quad_transition_on_axis(entry_wp: str, exit: str) -> str:
            sign: str = sign_manager(entry_wp, exit)
            for bound, signs in ON_AXIS_TRANS_LOGIC.items():
                if sign in signs:
                    return bound[0]

        def quad_transition_nz_axis(entry_wp: str, exit: str) -> str:
            wps: tuple[str, str] = ON_AXIS_NZ_TRANS_LOGIC[entry_wp]
            wp1: tuple[float, float] = WaypointUtils.get_waypoint_coords(wps[0].split("~")[-1])
            wp2: tuple[float, float] = WaypointUtils.get_waypoint_coords(wps[1].split("~")[-1])
            exit_coords: tuple[float, float] = WaypointUtils.get_waypoint_coords(exit.split("~")[-1])
            if WaypointUtils.dist_betw_two_coords(wp1, exit_coords) > WaypointUtils.dist_betw_two_coords(wp2, exit_coords):
                return (wps[1])
            else:
                return (wps[0])

        def landing(entry_wp: str, runway: str) -> str:
            if entry_wp in LANDING_LOGIC:
                if runway == '09 L':
                    return entry_wp + '~' + LANDING_LOGIC[entry_wp][0]
                elif runway == '27 R':
                    return entry_wp + '~' + LANDING_LOGIC[entry_wp][1]
            else:
                quad: int = determine_quadrant(WaypointUtils.get_waypoint_coords(entry_wp)[0], WaypointUtils.get_waypoint_coords(entry_wp)[1])
                if quad in [1, 2]:
                    if runway == '09 L':
                        return entry_wp + '~' + LANDING_LOGIC[quad][0]
                    else:
                        if entry_wp in WP_BOUND:
                            return entry_wp + '~' + WP_BOUND[entry_wp] + '~' + LANDING_LOGIC[quad][1]
                        else:
                            return entry_wp + '~' + LANDING_LOGIC[quad][1]
                else:
                    if runway == '09 L':
                        if entry_wp in WP_BOUND:
                            return entry_wp + '~' + WP_BOUND[entry_wp] + '~' + LANDING_LOGIC[quad][1]
                        else:
                            return entry_wp + '~' + LANDING_LOGIC[quad][1]
                    else:
                        return entry_wp + '~' + LANDING_LOGIC[quad][0]

        def path_trimmer(path: str) -> str:
            waypoints: list[str] = path.split('~')
            seen: set[str] = set()
            unique_waypoints: list[str] = []

            for waypoint in waypoints:
                if waypoint not in seen:
                    seen.add(waypoint)
                    unique_waypoints.append(waypoint)

            return '~'.join(unique_waypoints)

        def non_zero_non_vert(entry_wp: str, exit: str) -> str:
            path : str = ""
            if entry_wp in WP_BOUND:
                path += entry_wp + '~' + WP_BOUND[entry_wp] + '~'
            else:
                path += entry_wp + '~'
            path += quad_transition_nznv(entry_wp, exit) + '~'
            if exit in WP_BOUND:
                path += WP_BOUND[exit] + '~' + exit
            else:
                path += exit
            return path_trimmer(path)

        def non_zero_vert(entry_wp: str, exit: str) -> str:
            path: str = ""
            if entry_wp in WP_BOUND:
                path += entry_wp + '~' + WP_BOUND[entry_wp] + '~'
            else:
                path += entry_wp + '~'
            if entry_wp in WP_BOUND:
                path += quad_transition_nzv(WP_BOUND[entry_wp], exit) + '~'
            else:
                path += quad_transition_nzv(entry_wp, exit) + '~'
            if exit in WP_BOUND:
                path += WP_BOUND[exit] + '~' + exit
            else:
                path += exit
            return path_trimmer(path)

        def on_axis_zero(entry_wp: str, exit: str) -> str:
            path: str = ""
            path += entry_wp + '~'
            if f'{entry_wp}~{exit}' in QUAD_BOUND:
                path += QUAD_BOUND[f'{entry_wp}~{exit}'][0] + '~'
            else:
                path += quad_transition_on_axis(entry_wp, exit) + '~'
            path += exit
            return path_trimmer(path)

        def on_axis_nzwp(entry_wp: str, exit: str) -> str:
            path: str = ""
            path += entry_wp + '~'
            path += quad_transition_nz_axis(entry_wp, exit) + '~'
            if exit in WP_BOUND:
                path += WP_BOUND[exit] + '~' + exit
            else:
                path += exit
            return path_trimmer(path)

        if not landing_details[0]:
            heading: float = landing_details[1]
            exit: str = exit_wp(heading)
            wp1: tuple[float, float] = WaypointUtils.get_waypoint_coords(entry_wp)
            wp2: tuple[float, float] = WaypointUtils.get_waypoint_coords(exit.split("~")[-1])

            if 0 in wp1 and 0 in wp2:
                path: str = on_axis_zero(entry_wp, exit)
            elif 0 in wp1 and 0 not in wp2:
                path: str = on_axis_nzwp(entry_wp, exit)
            elif 0 in wp2 and 0 not in wp1:
                path: str = "~".join(on_axis_nzwp(exit, entry_wp).split("~")[::-1])
            elif (determine_quadrant(*wp1) + 2 != determine_quadrant(*wp2)) and ((determine_quadrant(*wp1) - 2) != determine_quadrant(*wp2)):
                path: str = non_zero_non_vert(entry_wp, exit)
            elif (determine_quadrant(*wp1) + 2 == determine_quadrant(*wp2)) or ((determine_quadrant(*wp1) - 2) == determine_quadrant(*wp2)):
                path: str = non_zero_vert(entry_wp, exit)
            else:
                ...
                return ""

            exit_coords: tuple[float, float] = WaypointUtils.get_entry_coords(155, landing_details[1])
            path += f'~{exit_coords}'
            return path

        else:
            path: str = landing(entry_wp, landing_details[1])
            path: str = path + f'~{(0,0)}~' + '~'.join(path.split('~')[::-1])
            return path
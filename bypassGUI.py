from aviary.interface.graphical_input import create_phase_info


class imitateTKboolvar():
    def __init__(self, value):
        self.value = True if value == "T" else False

    def get(self):
        return self.value


def bypassGUI(plane_name):
    plane_filename = f"planeCSVs/{plane_name}.csv"
    missions_idx = -1
    with open(plane_filename, 'r') as fp:
        data = fp.readlines()
        for i, line in enumerate(data):
            if "missions definition" in line.lower():
                missions_idx = i
    if missions_idx == -1:
        return 1

    missions = {}
    current_mission_key = ""
    for line in data[missions_idx+1:]:
        if len(line.split("#")) > 1:
            key, values = line.split("#")[1].strip().split(":")
            values = values.strip().split(",")
            if key == "mission_name":
                current_mission_key = values[0]
                missions[current_mission_key] = {}
            elif key == "times" or key == "altitudes" or key == "machs":
                missions[current_mission_key][key] = [
                    float(element) for element in values]
            elif key == "optimize_altitudes" or key == "optimize_machs":
                missions[current_mission_key][key] = [
                    imitateTKboolvar(item) for item in values]
            elif key == "takeoff" or key == "landing":
                missions[current_mission_key][key] = True if values[0] == "T" else False
            else:
                continue

    users = {'solve_for_distance': True, 'constrain_range': False}

    for mission_name, mission in missions.items():
        mission["num_segments"] = len(mission["times"])
        users["include_takeoff"] = mission["takeoff"]
        users["include_landing"] = mission["landing"]
        mission["phase_info"] = create_phase_info(
            times=mission["times"],
            altitudes=mission["altitudes"],
            mach_values=mission["machs"],
            polynomial_order=1, num_segments=mission["num_segments"],
            optimize_altitude_phase_vars=mission["optimize_altitudes"],
            optimize_mach_phase_vars=mission["optimize_machs"],
            user_choices=users, units=["min", "ft", "unitless"],
            orders=[3] * mission["num_segments"],
            filename=f"phase_info_{plane_name}_{mission_name}.py")
    return (missions, plane_filename)

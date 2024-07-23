"""
author: Jatin Soni
Bypasses Aviary Level 1 "draw_mission" GUI for creating phase_info dict
Runs aircraft model as an aviary problem
Prints important results for validating with known information about aircraft

run as: python aviaryPlane.py <airplane csv name>, e.g. python aviaryPlane.py testplane
"""
import sys
import os
import pandas as pd
import aviary.api as av
from bypassGUI import bypassGUI

# throttle enforcement options: 'path_constraint', 'boundary_constraint', 'bounded', None

# use provided plane name in cli to locate csv and find mission trajectory points
options = []
if len(sys.argv) > 1:
    planename = sys.argv[1]
    missions, plane_file = bypassGUI(planename)
    if len(sys.argv) > 2:
        options = sys.argv[2:]

else:
    raise Exception("No airplane name entered! E.g. python aviaryPlane.py planeName")

if not "rangecheck" in options and not "checkrange" in options:
    for key, mission in missions.items():
        if "only" in options:
            if not key in options:
                continue
        phase_info = mission["phase_info"]
        with open(f"planeCSVs/{planename}.csv", "r") as fp:
            with open("planeCSVs/tempav.csv", "w") as fd:
                lines = fp.readlines()
                for i, line in enumerate(lines):
                    if "aircraft:design:empty_mass" in line:
                        lines[i] = "# "+line
                    if "aircraft:crew_and_payload:cargo_mass" in line:
                        if key == "ferry":
                            lines[i] = line.split(",")[0]+",0,"+line.split(",")[2]
                        elif key == "morepayload":
                            lines[i] = line.split(",")[0]+",164900,"+line.split(",")[2]

                fd.writelines(lines)

        mission["prob_name"] = f"{planename}_{key}"
        mission["prob"] = av.run_aviary(
            "planeCSVs/tempav.csv", phase_info, optimizer="SLSQP", make_plots=True,
            max_iter=50, prob_name=mission["prob_name"])
        # mission["prob"].model.list_outputs() # way too many outputs

    printdata = []
    for key, mission in missions.items():
        if not "prob_name" in mission.keys():
            continue
        with open("reports/"+mission["prob_name"]+"/mission_summary.md", "r") as report:
            for line in report:
                if "Total Ground Distance" in line:
                    range = float(line.split("|")[2])

        df = pd.read_csv("reports/"+mission["prob_name"]+"/mission_timeseries_data.csv")
        firstthr = df['throttle (unitless)'][0]
        firstdrag = df['drag (lbf)'][0]
        prob = mission["prob"]

        vals = [range, firstthr, firstdrag,
                prob.get_val(av.Mission.Design.GROSS_MASS, units='lbm')[0],
                prob.get_val(av.Aircraft.Design.EMPTY_MASS, units='lbm')[0],
                prob.get_val(av.Aircraft.Design.TOTAL_WETTED_AREA, units='ft**2')[0],
                prob.get_val(av.Aircraft.Wing.WETTED_AREA, units='ft**2')[0],
                prob.get_val(av.Aircraft.Fuselage.WETTED_AREA, units='ft**2')[0],
                prob.get_val(av.Aircraft.HorizontalTail.WETTED_AREA, units='ft**2')[0],
                prob.get_val(av.Aircraft.VerticalTail.WETTED_AREA, units='ft**2')[0],
                prob.get_val(av.Aircraft.Nacelle.WETTED_AREA, units='ft**2')[0],
                prob.get_val(av.Aircraft.Wing.MASS, units='lbm')[0]]
        printdata.append(vals)

    print("=====================================================================")
    # print(dir(av.Aircraft)) -> list of attributes including __xx__ functions

    labels = [
        "Total range", "First throttle point", "First drag point", "Gross mass",
        "Empty mass", "Total wetted area", "Wing wetted area", "Fuselage wetted area",
        "Horizontal Tail wetted area", "Vertical Tail wetted area",
        "Nacelle wetted area", "Wing mass"]
    for row, label in enumerate(labels):
        if row == 0:
            names = []
            for mission in missions.values():
                try:
                    names.append(f"{mission['prob_name']:>16}")
                except KeyError:
                    continue
            titlestuff = ' | '.join(names)
            print(f"{'Problem Name':>30}: {titlestuff}")
            print("---------------------------------------------------------------------")
        unit = ""
        if "area" in label:
            unit = "sqft"
        elif "mass" in label:
            unit = "lbm"
        elif "range" in label:
            unit = "nmi"
        numstuff = ' | '.join(
            [f"{printdata[col][row]:10.2f} {unit:5s}" for col, _ in
             enumerate(printdata)])
        print(f"{labels[row]:>30}: {numstuff}")

    emptyMs = {"c17": 282500, "c40": 90000, "b757": 128840, "c5": 380e3}
    if planename in emptyMs.keys():
        error = (printdata[0][4]-emptyMs[planename])/emptyMs[planename]*100
        print(f"Empty mass error: {error:.2f}%")
    if "dashboard" in options:
        os.system("aviary dashboard "+planename)

# ----------
# extra code that may be useful

# from copy import deepcopy
# from outputted_phase_info import phase_info  # type: ignore

# FWFM_file = 'models/test_aircraft/aircraft_for_bench_FwFm.csv'
# myfile = 'mytestplane4.csv'

# av.default_height_energy_phase_info # default phase info object

# # process for adding reserve phase
# phase_info_res = deepcopy(phase_info)

# # Copy the current cruise phase, then make it a reserve phase
# reserve_phase_0 = deepcopy(phase_info_res['cruise_1'])
# reserve_phase_0['user_options']['reserve'] = True
# reserve_phase_0['user_options']['target_distance'] = (300, 'km')
# # remove the climb from the original cruise
# reserve_phase_0['user_options']['final_altitude'] = (32000.0, "ft")
# # This cruise is much shorter so we need to revise the duration_bounds for this phase
# reserve_phase_0['user_options']['duration_bounds'] = ((0, 120.0), "min")

# # Add the reserve phase to phase_info
# phase_info_res.update({'reserve_cruise': reserve_phase_0})

# print("=========================================================")
# print(f"-------------- Problem Name: {mission['prob_name']} -----")
# print(f"                Total range: {range:10.2f} nmi")
# print(f"       First throttle point: {firstthr:10.2f}")
# print(f"           First drag point: {firstdrag:10.2f} lbf")
# print(f"                 Gross mass: {prob.get_val(av.Mission.Design.GROSS_MASS,units='lbm')[0]:10.2f} lbm")
# print(f"                 Empty mass: {prob.get_val(av.Aircraft.Design.EMPTY_MASS,units='lbm')[0]:10.2f} lbm")
# print(f"          Total wetted area: {prob.get_val(av.Aircraft.Design.TOTAL_WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
# print(f"           Wing wetted area: {prob.get_val(av.Aircraft.Wing.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
# print(f"       Fuselage wetted area: {prob.get_val(av.Aircraft.Fuselage.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
# print(f"Horizontal Tail wetted area: {prob.get_val(av.Aircraft.HorizontalTail.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
# print(f"  Vertical Tail wetted area: {prob.get_val(av.Aircraft.VerticalTail.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
# print(f"        Nacelle wetted area: {prob.get_val(av.Aircraft.Nacelle.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")

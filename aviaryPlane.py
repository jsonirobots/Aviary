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
if len(sys.argv) > 1:
    planename = sys.argv[1]
    phase_info,plane_file = bypassGUI(planename)
    if len(sys.argv) > 2:
        option = sys.argv[2]

else:
    raise Exception("No airplane name entered! E.g. python aviaryPlane.py planeName")

prob = av.run_aviary(plane_file, phase_info,
                     optimizer="SLSQP", make_plots=True,max_iter = 50)

with open("reports/"+planename+"/mission_summary.md","r") as report:
    for line in report:
        if "Total Ground Distance" in line:
            range = float(line.split("|")[2])

df = pd.read_csv("reports/"+planename+"/mission_timeseries_data.csv")
firstthr = df['throttle (unitless)'][0]
firstdrag = df['drag (lbf)'][0]


print(f"                Total range: {range:10.2f} nmi")
print(f"       First throttle point: {firstthr:10.2f}")
print(f"           First drag point: {firstdrag:10.2f} lbf")
print(f"                 Gross mass: {prob.get_val(av.Mission.Design.GROSS_MASS,units='lbm')[0]:10.2f} lbm")
print(f"          Total wetted area: {prob.get_val(av.Aircraft.Design.TOTAL_WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
print(f"           Wing wetted area: {prob.get_val(av.Aircraft.Wing.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
print(f"       Fuselage wetted area: {prob.get_val(av.Aircraft.Fuselage.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
print(f"Horizontal Tail wetted area: {prob.get_val(av.Aircraft.HorizontalTail.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
print(f"  Vertical Tail wetted area: {prob.get_val(av.Aircraft.VerticalTail.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")
print(f"        Nacelle wetted area: {prob.get_val(av.Aircraft.Nacelle.WETTED_AREA,units='ft**2')[0]:10.2f} sqft")

if len(sys.argv) > 2:
    if option == "dashboard":
        os.system("aviary dashboard "+planename)

# ----------
# extra code that may be useful

# from copy import deepcopy
# from outputted_phase_info import phase_info  # type: ignore

#FWFM_file = 'models/test_aircraft/aircraft_for_bench_FwFm.csv'
#myfile = 'mytestplane4.csv'

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
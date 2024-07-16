from aviary.interface.graphical_input import create_phase_info

class imitateTKboolvar():
    def __init__(self,value):
        self.value = True if value == "T" else False
    def get(self):
        return self.value

def bypassGUI(plane_name):
    plane_filename = f"planeCSVs/{plane_name}.csv"
    missions_idx = -1
    with open(plane_filename,'r') as fp:
        data = fp.readlines()
        for i,line in enumerate(data):
            if "missions definition" in line.lower():
                missions_idx = i
    if missions_idx == -1:
        return 1
    
    missions = {}
    current_mission_key = ""
    for line in data[missions_idx+1:]:
        if len(line.split("#")) > 1:
            key,values = line.split("#")[1].strip().split(":")
            values = values.strip().split(",")
            if key == "mission_name":
                current_mission_key = values[0]
                missions[current_mission_key] = {}
            elif key == "times" or key == "altitudes" or key == "machs":
                missions[current_mission_key][key] = [float(element) for element in values]
            elif key == "optimize_altitudes" or key == "optimize_machs":
                missions[current_mission_key][key] = [imitateTKboolvar(item) for item in values]
            elif key == "takeoff" or key == "landing":
                missions[current_mission_key][key] = True if values[0] == "T" else False
            else: continue
        
    users = {'solve_for_distance':True,'constrain_range':False}

    for mission in missions.values():
        mission["num_segments"] = len(mission["times"])
        mission["phase_info"] = create_phase_info(times = mission["times"],altitudes = mission["altitudes"],
                                       mach_values = mission["machs"],polynomial_order = 1,
                                       num_segments = mission["num_segments"],
                                       optimize_altitude_phase_vars = mission["optimize_altitudes"],
                                       optimize_mach_phase_vars = mission["optimize_machs"],
                                       user_choices = users, takeoff = False, landing = False)
    return (missions,plane_filename)

# def bypassGUI(planename,polyord = 1,solvedist = False,constrainrange = True,segorder = 3):
    # directory = "planeCSVs/"
    # plane_file = directory+planename+".csv"
    # lines = []
    # with open(plane_file,'r') as fp:
    #     data = fp.readlines()
    #     try:
    #         idx = data.index("### mission definition\n")
    #     except ValueError:
    #         raise Exception("Mission definition not found in aircraft csv!")
    
    # for i,line in enumerate(data[idx+1:idx+8]):  
    #     lntmp = line.split(": ")[1].split("\n")[0].split(",")
    #     if i<3:
    #         lines.append([float(j) for j in lntmp])
    #     else:
    #         tf = [False,True]
    #         lines.append([tf[j=="T"] for j in lntmp])

    # times = lines[0]
    # alts  = lines[1]
    # machs = lines[2]
    # optalts = lines[3]
    # optmachs = lines[4]
    # takeoff = lines[5][0]
    # landing = lines[6][0]
    
    # numsegs  = len(times) -1 # num of segments

    # # fake tkinter boolean object to work with existing create phase info function
    # class tkbvreplica:
    #     def __init__(self, val): 
    #         self.val = val
    #     def get(self): # create_phase_info uses a .get function on tk boolean
    #         return self.val
    # optF = tkbvreplica(False)
    # optT = tkbvreplica(True)
    # opts = [optF,optT]
    
    # # if user does not provide, use false, otherwise substitute bool with tkinter replica
    # if not optmachs:
    #     optmachs = [optF for i in range(numsegs)]
    # else:
    #     if(len(optmachs)!=numsegs):
    #         raise Exception("Length of optimize mach/altitude list is incorrect!")
    #     optmachs = [opts[i] for i in optmachs]

    # if not optalts:
    #     optalts  = [optF for i in range(numsegs)]
    # else:        
    #     if(len(optalts)!=numsegs):
    #         raise Exception("Length of optimize mach/altitude list is incorrect!")
    #     optalts = [opts[i] for i in optalts]

    # users = {'solve_for_distance':solvedist,'constrain_range':constrainrange}

    # phase_info = create_phase_info(times,alts,machs,polyord,numsegs,optmachs,optalts,users,takeoff,landing)
   
    # # edit order in each phase, default is 3
    # if(segorder!=3):
    #     for phasedata in phase_info.values():
    #         if 'user_options' in phasedata:
    #             if 'order' in phasedata["user_options"]:
    #                 phasedata["user_options"]['order'] = segorder

    # return (phase_info,plane_file)
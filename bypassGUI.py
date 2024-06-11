from aviary.interface.graphical_input import create_phase_info

def bypassGUI(planename):
    directory = "planeCSVs/"
    plane_file = directory+planename+".csv"
    found = 0
    lines = []
    with open(plane_file,'r') as fp:
        for line in fp:
            if found > 0 and found < 4:
                lntmp = line.split(": ")[1].split(",")
                lines.append([float(i) for i in lntmp])
                found += 1 # 1 for times, ... 3 for machs
            if ("### mission definition" in line):
                found +=1 

    times = lines[0]
    alts  = lines[1]
    machs = lines[2]

    polyord  = 1    # polynomial order
    numsegs  = len(times) -1 # num of segments

    # fake tkinter boolean object to work with existing create phase info function
    class tkbvreplica:
        def __init__(self, val): 
            self.val = val
        def get(self): # create_phase_info uses a .get function on tk boolean
            return self.val
    optF = tkbvreplica(False)
    optT = tkbvreplica(True)
    optmachs = [optF,optF,optF]
    optalts  = [optF,optF,optF]

    users = {'solve_for_distance':False,'constrain_range':True}

    phase_info = create_phase_info(times,alts,machs,polyord,numsegs,optmachs,optalts,users)
   
    # edit order in each phase, default is 3
    for phasedata in phase_info.values():
        if 'user_options' in phasedata:
            if 'order' in phasedata["user_options"]:
                phasedata["user_options"]['order'] = 4

    return (phase_info,plane_file)
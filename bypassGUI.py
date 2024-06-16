from aviary.interface.graphical_input import create_phase_info

def bypassGUI(planename,polyord = 1,solvedist = False,constrainrange = True,segorder = 3):
    directory = "planeCSVs/"
    plane_file = directory+planename+".csv"
    lines = []
    with open(plane_file,'r') as fp:
        data = fp.readlines()
        try:
            idx = data.index("### mission definition\n")
        except ValueError:
            raise Exception("Mission definition not found in aircraft csv!")
    
    for i,line in enumerate(data[idx+1:idx+8]):  
        lntmp = line.split(": ")[1].split("\n")[0].split(",")
        if i<3:
            lines.append([float(j) for j in lntmp])
        else:
            tf = [False,True]
            lines.append([tf[j=="T"] for j in lntmp])

    times = lines[0]
    alts  = lines[1]
    machs = lines[2]
    optalts = lines[3]
    optmachs = lines[4]
    takeoff = lines[5][0]
    landing = lines[6][0]
    
    numsegs  = len(times) -1 # num of segments

    # fake tkinter boolean object to work with existing create phase info function
    class tkbvreplica:
        def __init__(self, val): 
            self.val = val
        def get(self): # create_phase_info uses a .get function on tk boolean
            return self.val
    optF = tkbvreplica(False)
    optT = tkbvreplica(True)
    opts = [optF,optT]
    
    # if user does not provide, use false, otherwise substitute bool with tkinter replica
    if not optmachs:
        optmachs = [optF for i in range(numsegs)]
    else:
        if(len(optmachs)!=numsegs):
            raise Exception("Length of optimize mach/altitude list is incorrect!")
        optmachs = [opts[i] for i in optmachs]

    if not optalts:
        optalts  = [optF for i in range(numsegs)]
    else:        
        if(len(optalts)!=numsegs):
            raise Exception("Length of optimize mach/altitude list is incorrect!")
        optalts = [opts[i] for i in optalts]

    users = {'solve_for_distance':solvedist,'constrain_range':constrainrange}

    phase_info = create_phase_info(times,alts,machs,polyord,numsegs,optmachs,optalts,users,takeoff,landing)
   
    # edit order in each phase, default is 3
    if(segorder!=3):
        for phasedata in phase_info.values():
            if 'user_options' in phasedata:
                if 'order' in phasedata["user_options"]:
                    phasedata["user_options"]['order'] = segorder

    return (phase_info,plane_file)
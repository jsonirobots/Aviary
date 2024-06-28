phase_info = {
    "pre_mission": {"include_takeoff": False, "optimize_mass": True},
    "climb_1": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "optimize_mach": False,
            "optimize_altitude": False,
            "polynomial_control_order": 1,
            "use_polynomial_control": True,
            "num_segments": 3,
            "order": 3,
            "solve_for_distance": False,
            "initial_mach": (0.3, "unitless"),
            "final_mach": (0.78, "unitless"),
            "mach_bounds": ((0.27999999999999997, 0.8), "unitless"),
            "initial_altitude": (0.0, "m"),
            "final_altitude": (10000.0, "m"),
            "altitude_bounds": ((0.0, 10500.0), "m"),
            "throttle_enforcement": "path_constraint",
            "fix_initial": True,
            "constrain_final": False,
            "fix_duration": False,
            "initial_bounds": ((0.0, 0.0), "min"),
            "duration_bounds": ((30.0, 90.0), "min"),
        },
        "initial_guesses": {"time": ([0, 60], "min")},
    },
    "cruise_1": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "optimize_mach": False,
            "optimize_altitude": False,
            "polynomial_control_order": 1,
            "use_polynomial_control": True,
            "num_segments": 3,
            "order": 3,
            "solve_for_distance": False,
            "initial_mach": (0.78, "unitless"),
            "final_mach": (0.78, "unitless"),
            "mach_bounds": ((0.76, 0.8), "unitless"),
            "initial_altitude": (10000.0, "m"),
            "final_altitude": (10000.0, "m"),
            "altitude_bounds": ((9500.0, 10500.0), "m"),
            "throttle_enforcement": "boundary_constraint",
            "fix_initial": False,
            "constrain_final": False,
            "fix_duration": False,
            "initial_bounds": ((30.0, 90.0), "min"),
            "duration_bounds": ((160.0, 480.0), "min"),
        },
        "initial_guesses": {"time": ([60, 320], "min")},
    },
    "descent_1": {
        "subsystem_options": {"core_aerodynamics": {"method": "computed"}},
        "user_options": {
            "optimize_mach": False,
            "optimize_altitude": False,
            "polynomial_control_order": 1,
            "use_polynomial_control": True,
            "num_segments": 3,
            "order": 3,
            "solve_for_distance": False,
            "initial_mach": (0.78, "unitless"),
            "final_mach": (0.3, "unitless"),
            "mach_bounds": ((0.27999999999999997, 0.8), "unitless"),
            "initial_altitude": (10000.0, "m"),
            "final_altitude": (0.0, "m"),
            "altitude_bounds": ((0.0, 10500.0), "m"),
            "throttle_enforcement": "path_constraint",
            "fix_initial": False,
            "constrain_final": True,
            "fix_duration": False,
            "initial_bounds": ((190.0, 570.0), "min"),
            "duration_bounds": ((15.0, 45.0), "min"),
        },
        "initial_guesses": {"time": ([380, 30], "min")},
    },
    "post_mission": {
        "include_landing": False,
        "constrain_range": True,
        "target_range": (3314, "nmi"),
    },
}

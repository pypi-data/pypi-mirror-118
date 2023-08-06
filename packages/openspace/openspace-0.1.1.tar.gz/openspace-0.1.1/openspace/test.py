from typing import final
import os
import sys

sys.path.append(os.getcwd())
import matplotlib.pyplot as plt
from openspace.math.coordinates import geodetic_to_geocentric, spherical_to_cartesian, get_rnp_matrix
from openspace.math.linear_algebra import Vector, Matrix
from openspace.math.measurements import Epoch, Angle, FinalsAll
from openspace.math.time_conversions import decimal_day_to_time
from configs.formats import STANDARD_EPOCH_FMT
from openspace.propagators.relative_motion import ClohessyWiltshireModel

FINALS_PATH = os.path.join("openspace","resources", "eop_data", "finals.all.csv")
if __name__=="__main__":
    
    state = Vector([0, -300000, 0, 0, 1, 0])
    cw_model = ClohessyWiltshireModel(state, 42164000)
    b1, b2, b3, t = cw_model.solve_three_burns_to_match_xy(86400*4)
    hp = cw_model.get_period()/2

    cw_model.apply_velocity_change(b1)
    cw_model = ClohessyWiltshireModel(cw_model.solve_next_state(hp), 42164000)
    cw_model.apply_velocity_change(b2)
    cw_model = ClohessyWiltshireModel(cw_model.solve_next_state(t), 42164000)
    #cw_model.apply_velocity_change(b3)

    r, i, c = cw_model.get_positions_over_interval(0, 86400, 600)
    plt.plot(i, r)
    plt.show()
    


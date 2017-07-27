import simshoy

a=simshoy.p_winning_in_rd1  # a dictionary
b=simshoy.p_winning_in_rd2  # an integer

a[(1,2)]=.8
a[(1,3)]=.97
a[(2,3)]=.8

simshoy.sim_SHOY(1000, a)

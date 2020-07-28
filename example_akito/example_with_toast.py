#!/usr/bin/env python3

import sa_tod
import sa_toast_tod

# You need 'input_name' attribute.
tod0 = sa_tod.TodNoToast({'input_name': 'data', 'bolo_time': 'this is boresight for tod0', 'det_1': 'this is det1 for tod 0'})
tod1 = sa_tod.TodNoToast({'input_name': 'mc_noise_1', 'bolo_time': 'this is boresight for tod1', 'det_1': 'this is det1 for tod 1'})

tod_list = sa_toast_tod.TodToastWrapper([tod0,tod1])

tod_list.set_tod_index(0)
print( tod_list.read_times() )

tod_list.set_tod_index(1)
print( tod_list.read_times() )

print( tod_list[1].read_times() )
print( tod_list[0].read_times() )

print( tod_list.read_times() )

print( tod_list.get_input_name_list() )

# Adding more.
tod2 = sa_tod.TodNoToast({'input_name': 'mc_noise_2', 'bolo_time': 'this is boresight for tod2', 'det_1': 'this is det1 for tod 2'})
tod3 = sa_tod.TodNoToast({'input_name': 'mc_noise_3', 'bolo_time': 'this is boresight for tod3', 'det_1': 'this is det1 for tod 3'})
tod4 = sa_tod.TodNoToast({'input_name': 'mc_noise_4', 'bolo_time': 'this is boresight for tod4', 'det_1': 'this is det1 for tod 4'})

tod_list2 = sa_toast_tod.TodToastWrapper([tod2,tod3,tod4])

tod_list3 = tod_list + tod_list2

print( tod_list3.get_input_name_list() )
print( tod_list3[3].read_times() )


print( tod_list.func_only_in_toast() )

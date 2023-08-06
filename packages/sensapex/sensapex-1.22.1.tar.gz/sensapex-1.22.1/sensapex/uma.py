import ctypes
from ctypes import (
    c_bool,
    c_int,
    c_int16,
    c_uint8,
    c_uint16,
    c_uint32,
    byref,
    POINTER,
    Structure,
)
from time import sleep

from sensapex.sensapex import um_state, UMP, LIBUM_MAX_MANIPULATORS

LIBUM_MAX_DEVS = 0xFFFF
UMA_REG_COUNT = 10


class uma_state(Structure):
    _fields_ = [
        ("um_ctx", POINTER(um_state)),
        ("um_dev", c_int),
        ("wait_trig", c_bool),
        ("reg_values", c_uint32 * UMA_REG_COUNT),
    ]


class uma_capture_struct(Structure):
    _fields_ = [
        ("status", c_uint8),
        ("flags", c_uint8),
        ("index", c_uint16),
        ("ts", c_uint32),
        ("current", c_int16),
        ("voltage", c_int16),
    ]


um = UMP.get_ump()
# LIBUM_SHARED_EXPORT int um_set_feature(um_state *hndl, const int dev, const int id, const int value);
for f in range(16):
    print(f"feature {f}: {um.call('um_get_feature', 1, f)}")
# um.call("um_set_feature", 1, 13, 1)
# print(f"feature 13: {um.call('um_get_feature', 1, 13)}")
# sleep(5)
# print(f"feature 13: {um.call('um_get_feature', 1, 13)}")
uma_state = uma_state()
lib = ctypes.cdll.LoadLibrary("/home/martin/src/acq4/uma-sdk/src/lib/libuma.so")
handle = um._um_state
print(um.list_devices())

devarray = (c_int * LIBUM_MAX_DEVS)()
lib.uma_get_device_list.restype = c_int
n_devs = lib.uma_get_device_list(byref(uma_state), byref(devarray), c_int(LIBUM_MAX_MANIPULATORS))
print([devarray[i] for i in range(n_devs)])

# handle = lib.uma_init(byref(state), handle, dev_id)
#
# lib.uma_set_range(byref(state), c_int(range))  # 200, 2000, 20000 or 200000
# lib.uma_set_sample_rate(byref(state), c_int(rate))  # 1221, 4883, 9776, 19531, 50000
# lib.uma_set_current_clamp_mode(byref(state), c_bool(True))
# lib.uma_set_vc_dac(byref(state), c_int16(value))
# lib.uma_set_trig_bit(byref(state), c_bool(False))
# lib.uma_set_wait_trig(byref(state), c_bool(False))

# Amplifier correction parameters
# lib.uma_set_vc_voltage_offset(byref(state), c_float(value))
# lib.uma_set_vc_cfast_gain(byref(state), c_float(value))
# lib.uma_set_vc_cslow_gain(byref(state), c_float(value))
# lib.uma_set_vc_cslow_tau(byref(state), c_float(value))
# lib.uma_set_vc_rs_corr_gain(byref(state), c_float(value))
# lib.uma_set_vc_rs_corr_tau(byref(state), c_float(value))
# lib.uma_enable_vc_rs_fast_lag_filter(byref(state), c_bool(value))
# lib.uma_enable_vc_rs_pred_3x_gain(byref(state), c_bool(value))
# lib.uma_enable_cc_higher_range(byref(state), c_bool(value))
# lib.uma_set_cc_dac(byref(state), c_int(value))
# lib.uma_set_cc_cfast_gain(byref(state), c_int(value))
# lib.uma_set_cc_bridge_gain(byref(state), c_int(value))

# Send command waveform
# values = (c_int() * N_SAMPLES)()
# lib.uma_stimulus(byref(state), c_int(N_SAMPLES), values, c_bool(trig));

# Start recording samples
# lib.uma_start(byref(state))
#
# buffer = (uma_capture_struct() * UMA_CAPTURES_PER_PACKET)()
# n_samples = lib.uma_recv(byref(state), UMA_CAPTURES_PER_PACKET, buffer)
#
# print(f"received {n_samples} samples")
#
# lib.uma_stop(byref(state))

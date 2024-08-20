from ctypes import *

""" Section: Constants """

""" Group: Error Codes
    SIDEKICK_SDK_RET_SUCCESS - Success error code. Compare return value from function with this value to check for success.
"""

MIRcatSDK_RET_SUCCESS = c_uint32(0)

""" Constants: Communication and Transport Errors
    MIRcatSDK_RET_UNSUPPORTED_TRANSPORT - If the user specified `commType` is invalid.
"""
MIRcatSDK_RET_UNSUPPORTED_TRANSPORT = c_uint32(1)

""" Constants: Initialization Errors
    MIRcatSDK_RET_INITIALIZATION_FAILURE - *[System Error]* If MIRcat controller Initialization failed.
"""
MIRcatSDK_RET_INITIALIZATION_FAILURE = c_uint32(32)

MIRcatSDK_RET_ARMDISARM_FAILURE = c_uint32(64)
MIRcatSDK_RET_STARTTUNE_FAILURE = c_uint32(65)
MIRcatSDK_RET_INTERLOCKS_KEYSWITCH_NOTSET = c_uint32(66)
MIRcatSDK_RET_STOP_SCAN_FAILURE = c_uint32(67)
MIRcatSDK_RET_PAUSE_SCAN_FAILURE = c_uint32(68)
MIRcatSDK_RET_RESUME_SCAN_FAILURE = c_uint32(69)
MIRcatSDK_RET_MANUAL_STEP_SCAN_FAILURE = c_uint32(70)
MIRcatSDK_RET_START_SWEEPSCAN_FAILURE = c_uint32(71)
MIRcatSDK_RET_START_STEPMEASURESCAN_FAILURE = c_uint32(72)
MIRcatSDK_RET_INDEX_OUTOFBOUNDS = c_uint32(73)
MIRcatSDK_RET_START_MULTISPECTRALSCAN_FAILURE = c_uint32(74)
MIRcatSDK_RET_TOO_MANY_ELEMENTS = c_uint32(75)
MIRcatSDK_RET_NOT_ENOUGH_ELEMENTS = c_uint32(76)
MIRcatSDK_RET_BUFFER_TOO_SMALL = c_uint32(77)
MIRcatSDK_RET_FAVORITE_NAME_NOTRECOGNIZED = c_uint32(78)
MIRcatSDK_RET_FAVORITE_RECALL_FAILURE = c_uint32(79)
MIRcatSDK_RET_WW_OUTOFTUNINGRANGE = c_uint32(80)
MIRcatSDK_RET_NO_SCAN_INPROGRESS = c_uint32(81)
MIRcatSDK_RET_EMISSION_ON_FAILURE = c_uint32(82)
MIRcatSDK_RET_EMISSION_ALREADY_OFF = c_uint32(83)
MIRcatSDK_RET_EMISSION_OFF_FAILURE = c_uint32(84)
MIRcatSDK_RET_EMISSION_ALREADY_ON = c_uint32(85)
MIRcatSDK_RET_PULSERATE_OUTOFRANGE = c_uint32(86)
MIRcatSDK_RET_PULSEWIDTH_OUTOFRANGE = c_uint32(87)
MIRcatSDK_RET_CURRENT_OUTOFRANGE = c_uint32(88)
MIRcatSDK_RET_SAVE_SETTINGS_FAILURE = c_uint32(89)
MIRcatSDK_RET_QCL_NUM_OUTOFRANGE = c_uint32(90)
MIRcatSDK_RET_LASER_ALREADY_ARMED = c_uint32(91)
MIRcatSDK_RET_LASER_ALREADY_DISARMED = c_uint32(92)
MIRcatSDK_RET_LASER_NOT_ARMED = c_uint32(93)
MIRcatSDK_RET_LASER_NOT_TUNED = c_uint32(94)
MIRcatSDK_RET_TECS_NOT_AT_SET_TEMPERATURE = c_uint32(95)
MIRcatSDK_RET_CW_NOT_ALLOWED_ON_QCL = c_uint32(96)
MIRcatSDK_RET_INVALID_LASER_MODE = c_uint32(97)
MIRcatSDK_RET_TEMPERATURE_OUT_OF_RANGE = c_uint32(98)
MIRcatSDK_RET_LASER_POWER_OFF_ERROR = c_uint32(99)
MIRcatSDK_RET_COMM_ERROR = c_uint32(100)
MIRcatSDK_RET_NOT_INITIALIZED = c_uint32(101)
MIRcatSDK_RET_ALREADY_CREATED = c_uint32(102)
MIRcatSDK_RET_START_SWEEP_ADVANCED_SCAN_FAILURE = c_uint32(103)
MIRcatSDK_RET_INJECT_PROC_TRIG_ERROR = c_uint32(104)


""" Group: Parameters """

""" Constant: Communication Parameters
    Parameters used to configure communication with MIRcat system.

    MIRcatSDK_COMM_SERIAL - Communication via Serial port.
    MIRcatSDK_COMM_UDP - Communication via UDP.
    MIRcatSDK_COMM_DEFAULT - Uses Serial Communication as the default.
"""
MIRcatSDK_COMM_SERIAL = c_uint8(1)
MIRcatSDK_COMM_UDP = c_uint8(2)
MIRcatSDK_COMM_DEFAULT = MIRcatSDK_COMM_SERIAL

""" Constant: Serial port parameters

    MIRcatSDK_SERIAL_PORT_AUTO - Automatically find the device on the port.
    MIRcatSDK_SERIAL_BAUD_USE_DEFAULT - desc
    MIRcatSDK_SERIAL_BAUD1 - desc
    MIRcatSDK_SERIAL_BAUD2 - desc
"""
MIRcatSDK_SERIAL_PORT_AUTO = c_uint16(0)
MIRcatSDK_SERIAL_BAUD_USE_DEFAULT = c_uint32(0)
MIRcatSDK_SERIAL_BAUD1 = c_uint16(115200)
MIRcatSDK_SERIAL_BAUD2 = c_uint16(921600)

""" Constant: Units
    Units for functions that use wavelength values.

    MIRcatSDK_UNITS_MICRONS - Micrometers, 1 x 10^-6 meters
    MIRcatSDK_UNITS_CM1 - Wavenumbers in cm^-1 units.  This is the spatial frequency of the wavelength and is in cycles per cm.
"""
MIRcatSDK_UNITS_MICRONS = c_uint8(1)
MIRcatSDK_UNITS_CM1 = c_uint8(2)

""" Group: Modes """

""" Constants: Laser Modes
    This is the mode the laser uses for emission.  Not all modes are supported by all laser heads

    MIRcatSDK_MODE_PULSED - Pulsed laser mode.  The laser pulses on/off at the set repetition rate and pulse width.
    MIRcatSDK_MODE_CW - Continuous Waveform Mode.  In this mode the laser emission is continuously on.
    MIRcatSDK_MODE_CW_MOD - Same as CW mode but with an analog modulation enable signal enabled.  This is only supported by laser heads that have a modulation enable input (such as MIRcat sleds).
    MIRcatSDK_MODE_CW_MR - Currently not supported in firmware.
    MIRcatSDK_MODE_CW_MR_MOD - Currently not supported in firmware.
    MIRcatSDK_MODE_CW_FLTR1 - desc
    MIRcatSDK_MODE_CW_FLTR2 - desc
    MIRcatSDK_MODE_CW_FLTR1_MOD - desc
"""

MIRcatSDK_MODE_ERROR = c_uint8(0)
MIRcatSDK_MODE_PULSED = c_uint8(1)
MIRcatSDK_MODE_CW = c_uint8(2)
MIRcatSDK_MODE_CW_MOD = c_uint8(3)
MIRcatSDK_MODE_CW_MR = c_uint8(6)  # currently not supported in firmware
MIRcatSDK_MODE_CW_MR_MOD = c_uint8(7)  # currently not supported in firmware
MIRcatSDK_MODE_CW_FLTR1 = c_uint8(8)
MIRcatSDK_MODE_CW_FLTR2 = c_uint8(9)
MIRcatSDK_MODE_CW_FLTR1_MOD = c_uint8(10)

""" Constant: Pulse Triggering Modes
    This is the laser triggering mode for controlling QCL on/off.

    MIRcatSDK_PULSE_MODE_INTERNAL - The laser internally controls pulse triggering based on set parameters.
    MIRcatSDK_PULSE_MODE_EXTERNAL_TRIGGER - The laser uses an external TTL trigger signal to control the start of a laser pulse.  The duration of the laser pulse is controlled by the laser pulse width setting.  A pulse is started on the rising edge of the external TTL signal with a jitter of up to 20 ns.
    MIRcatSDK_PULSE_MODE_EXTERNAL_PASSTHRU - This is similar to external trigger mode, but the laser output simply follows the external TTL signal, with limits.  CW lasers are not limited.  Pulsed only lasers are limited to BOTH their maximum pulse width and duty cycle.  This mode only uses combinational logic between the external TTL signal and the laser trigger enable to limit jitter to near zero.
    MIRcatSDK_PULSE_MODE_WAVELENGTH_TRIGGER - Description
"""
MIRcatSDK_PULSE_MODE_INTERNAL = c_uint8(1)
MIRcatSDK_PULSE_MODE_EXTERNAL_TRIGGER = c_uint8(2)
MIRcatSDK_PULSE_MODE_EXTERNAL_PASSTHRU = c_uint8(3)
MIRcatSDK_PULSE_MODE_WAVELENGTH_TRIGGER = c_uint8(4)

""" Constant: Process Triggering Modes
    For step scan modes (Step & Measure and Multi-Spectral) a process trigger is used to go to the next step in the scan.  The system provides the option to use three different types of process trigger modes below.

    MIRcatSDK_PROC_TRIG_MODE_INTERNAL - Laser controller controls all timing for step scan modes.
    MIRcatSDK_PROC_TRIG_MODE_EXTERNAL - External trigger on MIRcat 9-pin I/O connector must be provided to advance to next step.  Signal must be pulled low for ~250 ms to trigger a step.
    MIRcatSDK_PROC_TRIG_MODE_MANUAL  - Manual trigger command from PC must be sent to advance to next step.
"""
MIRcatSDK_PROC_TRIG_MODE_INTERNAL = c_uint8(1)
MIRcatSDK_PROC_TRIG_MODE_EXTERNAL = c_uint8(2)
MIRcatSDK_PROC_TRIG_MODE_MANUAL = c_uint8(3)


# Mapping error codes to their messages
error_messages = {
    MIRcatSDK_RET_UNSUPPORTED_TRANSPORT.value: "Unsupported transport type.",
    MIRcatSDK_RET_INITIALIZATION_FAILURE.value: "Initialization failure.",
    MIRcatSDK_RET_ARMDISARM_FAILURE.value: "Failed to arm/disarm the laser.",
    MIRcatSDK_RET_STARTTUNE_FAILURE.value: "Failed to start tuning.",
    MIRcatSDK_RET_INTERLOCKS_KEYSWITCH_NOTSET.value: "Interlocks or key switch not set.",
    MIRcatSDK_RET_STOP_SCAN_FAILURE.value: "Failed to stop the scan.",
    MIRcatSDK_RET_PAUSE_SCAN_FAILURE.value: "Failed to pause the scan.",
    MIRcatSDK_RET_RESUME_SCAN_FAILURE.value: "Failed to resume the scan.",
    MIRcatSDK_RET_MANUAL_STEP_SCAN_FAILURE.value: "Failed to manually step scan.",
    MIRcatSDK_RET_START_SWEEPSCAN_FAILURE.value: "Failed to start sweep scan.",
    MIRcatSDK_RET_START_STEPMEASURESCAN_FAILURE.value: "Failed to start step-measure scan.",
    MIRcatSDK_RET_INDEX_OUTOFBOUNDS.value: "Index out of bounds.",
    MIRcatSDK_RET_START_MULTISPECTRALSCAN_FAILURE.value: "Failed to start multi-spectral scan.",
    MIRcatSDK_RET_TOO_MANY_ELEMENTS.value: "Too many elements specified.",
    MIRcatSDK_RET_NOT_ENOUGH_ELEMENTS.value: "Not enough elements specified.",
    MIRcatSDK_RET_BUFFER_TOO_SMALL.value: "Buffer too small.",
    MIRcatSDK_RET_FAVORITE_NAME_NOTRECOGNIZED.value: "Favorite name not recognized.",
    MIRcatSDK_RET_FAVORITE_RECALL_FAILURE.value: "Failed to recall favorite.",
    MIRcatSDK_RET_WW_OUTOFTUNINGRANGE.value: "Wavelength out of tuning range.",
    MIRcatSDK_RET_NO_SCAN_INPROGRESS.value: "No scan in progress.",
    MIRcatSDK_RET_EMISSION_ON_FAILURE.value: "Failed to turn emission on.",
    MIRcatSDK_RET_EMISSION_ALREADY_OFF.value: "Emission already off.",
    MIRcatSDK_RET_EMISSION_OFF_FAILURE.value: "Failed to turn emission off.",
    MIRcatSDK_RET_EMISSION_ALREADY_ON.value: "Emission already on.",
    MIRcatSDK_RET_PULSERATE_OUTOFRANGE.value: "Pulse rate out of range.",
    MIRcatSDK_RET_PULSEWIDTH_OUTOFRANGE.value: "Pulse width out of range.",
    MIRcatSDK_RET_CURRENT_OUTOFRANGE.value: "Current out of range.",
    MIRcatSDK_RET_SAVE_SETTINGS_FAILURE.value: "Failed to save settings.",
    MIRcatSDK_RET_QCL_NUM_OUTOFRANGE.value: "QCL number out of range.",
    MIRcatSDK_RET_LASER_ALREADY_ARMED.value: "Laser already armed.",
    MIRcatSDK_RET_LASER_ALREADY_DISARMED.value: "Laser already disarmed.",
    MIRcatSDK_RET_LASER_NOT_ARMED.value: "Laser not armed.",
    MIRcatSDK_RET_LASER_NOT_TUNED.value: "Laser not tuned.",
    MIRcatSDK_RET_TECS_NOT_AT_SET_TEMPERATURE.value: "TEC not at set temperature.",
    MIRcatSDK_RET_CW_NOT_ALLOWED_ON_QCL.value: "CW not allowed on specified QCL.",
    MIRcatSDK_RET_INVALID_LASER_MODE.value: "Invalid laser mode.",
    MIRcatSDK_RET_TEMPERATURE_OUT_OF_RANGE.value: "Temperature out of range.",
    MIRcatSDK_RET_LASER_POWER_OFF_ERROR.value: "Failed to power off the laser.",
    MIRcatSDK_RET_COMM_ERROR.value: "Communication error.",
    MIRcatSDK_RET_NOT_INITIALIZED.value: "SDK not initialized.",
    MIRcatSDK_RET_ALREADY_CREATED.value: "Instance already created.",
    MIRcatSDK_RET_START_SWEEP_ADVANCED_SCAN_FAILURE.value: "Failed to start advanced sweep scan.",
    MIRcatSDK_RET_INJECT_PROC_TRIG_ERROR.value: "Failed to inject process trigger.",
    MIRcatSDK_MODE_ERROR.value: "Invalid laser mode specified.",
}

import os
import sys
import platform
import time
from functools import wraps
from ctypes import CDLL, c_uint16, c_uint8, c_float, c_bool, byref
from mircatpy.MIRcatSDKConstants import *
import threading

from colorama import Fore, Style, init


class MIRcatError(Exception):
    def __init__(self, code, message="Error occurred with MIRcatSDK"):
        self.code = code
        self.message = message
        super().__init__(self.message)


def requires_connection(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_connected():
            raise MIRcatError(
                code="-3", message="Operation requires connection to MIRCat laser."
            )
        return func(self, *args, **kwargs)

    return wrapper


def check_return_value(ret, success_code=MIRcatSDK_RET_SUCCESS.value):
    """
    Checks if the return value indicates success or failure and raises an exception with a descriptive message.

    :param ret: The return value to check.
    :param success_code: The value that indicates success. Default is MIRcatSDK_RET_SUCCESS.value.
    :raises MIRcatSDKError: If the return value does not indicate success.
    """
    if ret != success_code:
        error_message = error_messages.get(ret, "Unknown error occurred")
        raise MIRcatError(ret, error_message)
    return True


def call_with_timeout(sdk_function, timeout=5, *args):
    """
    Calls an SDK function with a timeout and checks the result.

    :param sdk_function: The SDK function to call (e.g., self.SDK.MIRcatSDK_GetNumInstalledQcls).
    :param timeout: The maximum time (in seconds) to allow for the function call.
    :param args: The arguments to pass to the SDK function.
    :return: The result of the SDK function call if successful, or None if it fails or times out.
    :raises MIRcatError: If the function call fails or times out.
    """

    def call_sdk():
        ret = sdk_function(*args)
        return check_return_value(ret)

    # Create a thread to run the SDK function
    sdk_thread = threading.Thread(target=call_sdk)

    # Start the thread
    sdk_thread.start()

    # Wait for the thread to complete or timeout
    sdk_thread.join(timeout)

    if sdk_thread.is_alive():
        # If still alive, we assume the call timed out
        raise MIRcatError(code="-2", message="SDK call timed out.")


def wait_till(function, target=True, delay=0.5, timeout=10):
    start_time = time.time()
    progress_bar_length = 30  # Length of the progress bar
    func_name = function.__name__

    print(f"Waiting for target value {target}...")

    while True:
        current_value = function()
        if current_value == target:
            print(f"\r{func_name} [{'█' * progress_bar_length}] 100% - Done!")
            return True

        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            print(f"\r{func_name} [{'█' * progress_bar_length}] Timeout!")
            raise TimeoutError(
                f"Timed out after {timeout} seconds while waiting for target value {target}."
            )

        # Calculate progress and display progress bar
        progress = min(
            int((elapsed_time / timeout) * progress_bar_length), progress_bar_length
        )
        progress_bar = "█" * progress + "-" * (progress_bar_length - progress)
        percent_complete = int((elapsed_time / timeout) * 100)

        print(f"\r{func_name} [{progress_bar}] {percent_complete}%", end="", flush=True)
        time.sleep(delay)


class MIRcat:
    def __init__(self, dll_path=None):
        if dll_path is None:
            dir = os.path.dirname(sys.modules["mircatpy"].__file__)

            # Check the architecture of the current Python interpreter
            arch = platform.architecture()[0]
            if arch == "64bit":
                dll_path = os.path.join(dir, "libs/x64/MIRcatSDK.dll")
            else:
                dll_path = os.path.join(dir, "libs/x32/MIRcatSDK.dll")

        self.SDK = CDLL(dll_path)
        self._initialize()

    def _initialize(self):
        init()
        self._get_api_version()
        self._status = {
            "connected": False,
            "numQCLs": "?",
            "isInterlockSet": "?",
            "isKeySwitchSet": "?",
            "isEmitting": "?",
            "isArmed": "?",
            "isTuned": "?",
            "wl": "?",
            "wn": "?",
        }

        self._scan_status = {
            "isScanInProgress": "?",
            "isScanActive": "?",
            "isScanPaused": "?",
            "curScanRepetition": "?",
            "curScanPercent": "?",
            "curWW": "?",
            "units": "?",
            "isTECInProgress": "?",
            "isMotionInProgress": "?",
            "wl": "?",
            "wn": "?",
        }

    def _get_api_version(self):
        major = c_uint16()
        minor = c_uint16()
        patch = c_uint16()
        call_with_timeout(
            self.SDK.MIRcatSDK_GetAPIVersion,
            5,
            byref(major),
            byref(minor),
            byref(patch),
        )
        self.APIversion = f"{major.value}.{minor.value}.{patch.value}"

    def connect(self):
        call_with_timeout(self.SDK.MIRcatSDK_Initialize, 5)
        return wait_till(self.is_connected)

    def is_connected(self):
        isConnected = c_bool(False)
        call_with_timeout(self.SDK.MIRcatSDK_IsConnectedToLaser, 5, byref(isConnected))
        return isConnected.value

    @requires_connection
    def disconnect(self):
        call_with_timeout(self.SDK.MIRcatSDK_DeInitialize, 5)
        return wait_till(self.is_connected, False)

    @property
    def status(self):
        if self.is_connected():
            self._status["numQCLs"] = self.get_num_qcls()
            self._status["isInterlockSet"] = self.get_interlock_status()
            self._status["isKeySwitchSet"] = self.get_key_switch_status()
            self._status["isArmed"] = self.get_laser_armed_status()
            self._status["isEmitting"] = self.check_laser_emission()
            self._status["isTuned"] = self.is_tuned()
            self._status["wl"], self._status["wn"] = self.get_ww()
        else:
            self._status["connected"] = False
        return self._status

    def display_status(self):
        print_dict(self.status)

    def display_scanStatus(self):
        print_dict(self.scanStatus)

    @requires_connection
    def get_num_qcls(self):
        numQCLs = c_uint8(0)
        call_with_timeout(self.SDK.MIRcatSDK_GetNumInstalledQcls, 5, byref(numQCLs))
        self.numQCLs = numQCLs.value
        return self.numQCLs

    @requires_connection
    def get_interlock_status(self):
        isInterlockSet = c_bool(False)
        call_with_timeout(
            self.SDK.MIRcatSDK_IsInterlockedStatusSet, 5, byref(isInterlockSet)
        )
        self.isInterlockSet = isInterlockSet.value
        return self.isInterlockSet

    @requires_connection
    def get_key_switch_status(self):
        isKeySwitchSet = c_bool(False)
        call_with_timeout(
            self.SDK.MIRcatSDK_IsKeySwitchStatusSet, 5, byref(isKeySwitchSet)
        )
        self.isKeySwitchSet = isKeySwitchSet.value
        return self.isKeySwitchSet

    @requires_connection
    def arm_laser(self):
        call_with_timeout(self.SDK.MIRcatSDK_ArmLaser, 5)
        return wait_till(self.get_laser_armed_status)

    @requires_connection
    def disarm_laser(self):
        call_with_timeout(self.SDK.MIRcatSDK_DisArmLaser, 5)
        return wait_till(self.get_laser_armed_status, False)

    @requires_connection
    def tune(self, mode, target):
        modes = {"wl": MIRcatSDK_UNITS_MICRONS, "wn": MIRcatSDK_UNITS_CM1}
        call_with_timeout(
            self.SDK.MIRcatSDK_TuneToWW, 5, c_float(target), modes.get(mode), c_uint8(1)
        )
        wait_till(self.is_tuned, True, 0.5, 30)

    @requires_connection
    def is_tuned(self):
        isTuned = c_bool(False)
        call_with_timeout(self.SDK.MIRcatSDK_IsTuned, 5, byref(isTuned))
        self._status["isTuned"] = isTuned.value
        return self._status["isTuned"]

    @requires_connection
    def get_ww(self):
        actualWW = c_float()
        lightValid = c_bool()
        units = c_uint8()

        call_with_timeout(
            self.SDK.MIRcatSDK_GetActualWW,
            5,
            byref(actualWW),
            byref(units),
            byref(lightValid),
        )
        self._status["wl"], self._status["wn"] = self._ww_interpreter(actualWW, units)

        return self._status["wl"], self._status["wn"]

    def _ww_interpreter(self, val, unit):
        if unit.value == MIRcatSDK_UNITS_MICRONS.value:
            wl = val.value
            wn = wl and 1e4 / wl or 0
        else:
            wn = val.value
            wl = wn and 1e4 / wn or 0
        return wl, wn

    @requires_connection
    def enable_emission(self):
        call_with_timeout(self.SDK.MIRcatSDK_TurnEmissionOn, 5)
        return wait_till(self.check_laser_emission)

    @requires_connection
    def disable_emission(self):
        call_with_timeout(self.SDK.MIRcatSDK_TurnEmissionOff, 5)
        return wait_till(self.check_laser_emission, False)

    @requires_connection
    def check_laser_emission(self):
        isEmitting = c_bool(False)
        call_with_timeout(self.SDK.MIRcatSDK_IsEmissionOn, 5, byref(isEmitting))
        self._status["isEmitting"] = isEmitting.value
        return self._status["isEmitting"]

    @requires_connection
    def get_laser_armed_status(self):
        isArmed = c_bool(True)
        call_with_timeout(self.SDK.MIRcatSDK_IsLaserArmed, 5, byref(isArmed))
        self._status["isArmed"] = isArmed.value
        return self._status["isArmed"]

    @requires_connection
    def get_QCL_params_all(self):
        res = []
        for QCLnum in [1, 2, 3, 4]:
            res += [self.get_QCL_params(QCLnum)]
        return res

    @requires_connection
    def get_QCL_PulseRate(self, QCLnum):
        QCLnum = c_uint8(QCLnum)
        puls_rate = c_float()
        call_with_timeout(
            self.SDK.MIRcatSDK_GetQCLPulseRate, 5, QCLnum, byref(puls_rate)
        )
        return puls_rate.value

    @requires_connection
    def get_QCL_PulseWidth(self, QCLnum):
        QCLnum = c_uint8(QCLnum)
        puls_width = c_float()
        call_with_timeout(
            self.SDK.MIRcatSDK_GetQCLPulseWidth, 5, QCLnum, byref(puls_width)
        )
        return puls_width.value

    @requires_connection
    def get_QCL_Current(self, QCLnum):
        QCLnum = c_uint8(QCLnum)
        current = c_float()
        call_with_timeout(self.SDK.MIRcatSDK_GetQCLCurrent, 5, QCLnum, byref(current))
        return current.value

    @requires_connection
    def get_QCL_params(self, QCLnum):
        return {
            "QCLnum": QCLnum,
            "puls_rate": self.get_QCL_PulseRate(QCLnum),
            "puls_width": self.get_QCL_PulseWidth(QCLnum),
            "current": self.get_QCL_Current(QCLnum),
        }

    @requires_connection
    def set_QCL_params(self, QCLnum, puls_rate, puls_width, current):
        duty_cycle = 1e-6 * puls_rate * puls_width

        if QCLnum not in [1, 2, 3, 4]:
            raise MIRcatError(-1, "Wrong QCLnum: must be one of 1,2,3,4")

        if puls_rate < 10 or puls_rate > 100000:
            raise MIRcatError(-1, "Puls rate limit: 10 <= puls rate <= 100000")

        if duty_cycle < 0 or duty_cycle > 5:
            raise MIRcatError(-1, "Duty cycle limit: 0% <= duty cycle <= 5%")

        if puls_width < 0 or puls_width > 100:
            raise MIRcatError(-1, "Duty cycle limit: 0 <= puls width <= 100")

        # Estimated from default values + 10%
        cur_limits = [800, 820, 630, 950]
        if current < 0 or current > cur_limits[QCLnum]:
            raise MIRcatError(
                -1, f"Current limit: 0 <= current <= {cur_limits[QCLnum]}"
            )

        call_with_timeout(
            self.SDK.MIRcatSDK_SetQCLParams,
            5,
            c_uint8(QCLnum),
            c_float(puls_rate),
            c_float(puls_width),
            c_float(current),
        )

    @requires_connection
    def startSweepScan(
        self, mode, start, end, speed, repetitions=1, bidirectional=False
    ):
        modes = {"wl": MIRcatSDK_UNITS_MICRONS, "wn": MIRcatSDK_UNITS_CM1}
        call_with_timeout(
            self.SDK.MIRcatSDK_StartSweepScan,
            5,
            c_float(start),
            c_float(end),
            c_float(speed),
            modes.get(mode),
            c_uint16(repetitions),
            c_bool(bidirectional),
        )

    @requires_connection
    def stopScan(self):
        call_with_timeout(self.SDK.MIRcatSDK_StopScanInProgress, 5)

    @requires_connection
    def pauseScan(self):
        call_with_timeout(self.SDK.MIRcatSDK_PauseScanInProgress, 5)

    @requires_connection
    def resumeScan(self):
        call_with_timeout(self.SDK.MIRcatSDK_ResumeScanInProgress, 5)

    @property
    @requires_connection
    def scanStatus(self):
        isScanInProgress = c_bool()
        isScanActive = c_bool()
        isScanPaused = c_bool()
        curScanRepetition = c_uint16()
        curScanPercent = c_uint16()
        curWW = c_float()
        units = c_uint8()
        isTECInProgress = c_bool()
        isMotionInProgress = c_bool()

        call_with_timeout(
            self.SDK.MIRcatSDK_GetScanStatus,
            5,
            byref(isScanInProgress),
            byref(isScanActive),
            byref(isScanPaused),
            byref(curScanRepetition),
            byref(curScanPercent),
            byref(curWW),
            byref(units),
            byref(isTECInProgress),
            byref(isMotionInProgress),
        )

        wl, wn = self._ww_interpreter(curWW, units)

        self._scan_status = {
            "isScanInProgress": isScanInProgress.value,
            "isScanActive": isScanActive.value,
            "isScanPaused": isScanPaused.value,
            "curScanRepetition": curScanRepetition.value,
            "curScanPercent": curScanPercent.value,
            "curWW": curWW.value,
            "isTECInProgress": isTECInProgress.value,
            "isMotionInProgress": isMotionInProgress.value,
            "wl": wl,  # Wavelength interpreted from curWW
            "wn": wn,  # Wavenumber interpreted from curWW
        }

        return self._scan_status

    def __del__(self):
        self.disconnect()

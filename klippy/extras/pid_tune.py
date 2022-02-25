# Tuning of heater PID parameters
#
# Copyright (C) 2016-2018  Kevin O'Connor <kevin@koconnor.net>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import math
import logging
from . import heaters


class PIDTune:
    def __init__(self, config):
        self.printer = config.get_printer()
        gcode = self.printer.lookup_object('gcode')
        gcode.register_command('PID_SET_GAINS', self.cmd_PID_SET_GAINS,
                               desc=self.cmd_PID_SET_GAINS_help)

    cmd_PID_SET_GAINS_help = "Run PID calibration test"

    def cmd_PID_SET_GAINS(self, gcmd):
        heater_name = gcmd.get('HEATER')

        pheaters = self.printer.lookup_object('heaters')
        try:
            heater = pheaters.lookup_heater(heater_name)
        except self.printer.config_error as e:
            raise gcmd.error(str(e))

        if not isinstance(heater.control, heaters.ControlPID):
            raise gcmd.error("Not PID control!")

        try:
            heater.control.Kp = gcmd.get_float('P') / heaters.PID_PARAM_BASE
        except Exception:
            pass
        try:
            heater.control.Ki = gcmd.get_float('I') / heaters.PID_PARAM_BASE
        except Exception:
            pass
        try:
            heater.control.Kd = gcmd.get_float('D') / heaters.PID_PARAM_BASE
        except Exception:
            pass

        gcmd.respond_info(
            "New PID parameters: pid_Kp=%.3f pid_Ki=%.3f pid_Kd=%.3f."
            % (heater.control.Kp * heaters.PID_PARAM_BASE,
               heater.control.Ki * heaters.PID_PARAM_BASE,
               heater.control.Kd * heaters.PID_PARAM_BASE))


def load_config(config):
    return PIDTune(config)

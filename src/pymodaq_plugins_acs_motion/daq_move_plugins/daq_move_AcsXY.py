
from typing import Union, List, Dict
from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun,
                                                          main, DataActuatorType, DataActuator)

from pymodaq_gui.parameter import Parameter

try:
    from pymodaq_plugins_acs_motion.hardware.acscontrol import Controller  # ACS controller wrapper
except AttributeError as e:  # the vendor library acspy uses ctypes.windll, which only exists on Windows
    raise ImportError('The acspy library is only usable on Windows') from e


class DAQ_Move_AcsXY(DAQ_Move_base):
    """ Minimalistic plugin to control ACS motion stages with PyMoDAQ.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    Use the ACSpy package wrapper to communicate with the ACS motion stages. 
    It may works with up to 8 axes depending the configuration.
    It does not consider the daisy chain option: only one controller.
    Only ETHERNET communication is implemented (see ACS manual for configuration).
    (It has been tested with USB to ethernet adapter).
    Tested with ACS SPiiPlusEC controller and one drive UDMnt(2 axes).
    The stages were alio's translation stages  AI-CM-6000-XY.
    PyMoDAQ version during the test was PyMoDAQ==5.0.5.
    The operating system used was Windows 11.
    Installation instructions: ACS drivers must be installed from the manufacturer's.
    They usually come with the controller and with a "buffer" file for coniguration.
    
  
    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.

    """
    is_multiaxes = True
    # Configured for two axes, can be extended up to 8 axes.
    _axis_names: Union[List[str], Dict[str, int]] = {'Axis0': 0, 'Axis1': 1}
    # All axes are translation stages here; adapt per axis if stages of different types are used.
    _controller_units: Union[str, Dict[str, str]] = {'Axis0': 'mm', 'Axis1': 'mm'}
    # Tolerance used to decide that the target is reached; refer to your stages for a meaningful value.
    _epsilons: Union[float, Dict[str, float]] = {'Axis0': 0.00001, 'Axis1': 0.00001}
    data_actuator_type = DataActuatorType.DataActuator
    
    params = [ {'title': 'Serial Number', 'name': 'serial_num', 'type': 'str', 
                'value': '', 'readonly': True,},
                {'title': 'Buffer Number', 'name': 'buff_num', 'type': 'int', 
                'value': 1, 'limits': [0, 9],}  
                ] + comon_parameters_fun(is_multiaxes, axis_names=_axis_names)

    def ini_attributes(self):
        self.controller: Controller = None

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        
        pos = DataActuator(data=self.controller.axes[self.axis_value].rpos,
                           units=self.axis_unit) 
        pos = self.get_position_with_scaling(pos)
        return pos

    def close(self):
        """Terminate the communication protocol"""
        if self.controller is not None:
            self.controller.disable_all()
            self.controller.disconnect()

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        if param.name() == 'axis':
            self.get_actuator_value()  # update the current position of the newly selected axis

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        
        self.ini_stage_init(slave_controller=controller)  # will be useful when controller is slave

        if self.is_master:  # is needed when controller is master
            self.controller = Controller(contype="ethernet", n_axes=2) 
            self.controller.connect()  # any object that will control the stages
            self.controller.enable_all()  # enable all axes
            self.settings['serial_num']=self.controller.serial_number()
            
          
        info = "Controller connected and axis enabled"
        initialized = all(axis.enabled for axis in self.controller.axes)
        return info, initialized

    def move_abs(self, value: DataActuator):
        """Move the actuator to the absolute target defined by value"""
        value = self.check_bound(value)
        self.target_value = value
        value = self.set_position_with_scaling(value)
        self.controller.axes[self.axis_value].ptp(value.units_as(self.axis_unit).value())

    def move_rel(self, value: DataActuator):
        """Move the actuator by the relative amount defined by value"""
        self.move_abs(self.current_value + value)

    def move_home(self):
        """Move the current axis back to position 0"""
        self.move_abs(DataActuator(data=0, units=self.axis_unit))    

    def stop_motion(self):
        """Stop the current axis and emit the move_done signal"""
        self.controller.axes[self.axis_value].halt()
        self.move_done()


if __name__ == '__main__':
    main(__file__)

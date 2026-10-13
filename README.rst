pymodaq_plugins_acs_motion
##########################

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_acs_motion.svg
   :target: https://pypi.org/project/pymodaq_plugins_acs_motion/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: PyMoDAQ Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_acs_motion/actions/workflows/python-publish.yml/badge.svg
   :target: https://github.com/PyMoDAQ/pymodaq_plugins_acs_motion/actions/workflows/python-publish.yml
   :alt: Publication Status

PyMoDAQ plugins for the ACS motion control unit.

Authors
=======

* Jérémie Margueritat (jeremie.margueritat@univ-lyon1.fr)

Instruments
===========

Below is the list of instruments included in this plugin.

Actuators
+++++++++

* **ACS motion control**: control up to 8 stages.

It has been developed with an ACS motion control unit SPiiPlusEC, linked with a two-axis driver
(amplifier) UDMnt. The stages were ALIO AI-CM-6000-XY translation stages.

Installation instructions
=========================

The user has to install the drivers from ACS. The homing program provided with the stages
must be stored in a buffer of the controller (buffer 1 by default, set with the
'Homing buffer' parameter of the plugin). The plugin never modifies the buffers of the
controller: the Home button runs the homing program and waits for its end, homing all the
axes at once. It is recommended to keep a full backup of the controller application, made
with the Application Wizard of SPiiPlus MMI Application Studio. Users are encouraged to check
the compatibility of their ACS hardware with the latest version of the plugin, and to refer
to the ACS documentation for any specific setup requirements.

* PyMoDAQ's version: tested with PyMoDAQ 5.3.2 (see pyproject.toml for the minimum required version)
* Operating system's version: Windows 11
* The plugin assumes that the ACS drivers are installed.
# Zaber Stage Control for Brain Phantom Experiments

## Overview

This project uses Python to control Zaber motorized stages for a brain phantom setup used in PET imaging research. The system allows for controlled movement and positioning of a brain phantom to explore different positions, orientations, and motion patterns.

The code includes functions for linear and rotational movement, multi-axis coordination, position management, and motion control. These capabilities help simulate different types of head movement and adjust the brain phantom's position during experimental testing.

## Project Objectives

- Control Zaber linear and rotational stages through Python.
- Adjust the position and orientation of a brain phantom.
- Coordinate movement across multiple axes.
- Experiment with different motion patterns, including linear, rotational, spiral, and other programmed trajectories where supported.
- Develop repeatable stage movements for brain phantom positioning and PET imaging experiments.

## Features

- **Linear stage control:** Adjust the brain phantom's position along a linear axis.
- **Rotational stage control:** Rotate the phantom to different angles and orientations.
- **Multi-device control:** Communicate with multiple Zaber devices.
- **Coordinated movement:** Explore simultaneous movement across multiple axes.
- **Motion simulation:** Program different movement patterns to investigate controlled phantom motion.
- **Position management:** Save and load position-related data or configurations.
- **Unit conversions:** Convert movement values into units appropriate for stage control.
- **Error handling:** Handle potential issues during device communication and motion control.

## Project Structure

| File                            | Description                                            |
| ------------------------------- | ------------------------------------------------------ |
| `main.py`                       | Main stage control and movement program                |
| `final_without_movement.py`     | Final program variant without executing stage movement |
| `get_started.py`                | Basic setup and control examples                       |
| `Controlling_mult_devices.py`   | Control multiple Zaber devices                         |
| `simultaneous_axis_movement.py` | Coordinate movement across multiple axes               |
| `rotation.py`                   | Control rotational stage movement                      |
| `Arbitrary_unit_conversions.py` | Convert between movement units                         |
| `Saving_and_loading.py`         | Save and load position or configuration data           |
| `load_and_save_ex.py`           | Examples of saving and loading data                    |
| `error_handling.py`             | Handle potential control and communication errors      |
| `G-code.py`                     | G-code-related movement commands                       |
| `Gcode.txt`                     | G-code examples or instructions                        |
| `Stages_SOP.pdf`                | Standard operating procedure for the stages            |
| `practice.py`                   | Practice and testing code                              |
| `v0.py`                         | Earlier version of the program                         |

## Technologies Used

- **Python** — Motion-control programming
- **Zaber motorized stages** — Precise linear and rotational positioning
- **Zaber Motion Library** — Device communication and motion control, if used by the scripts

## Acknowledgments

Developed as part of a brain phantom motion-control project involving Zaber motorized stages and Python programming for PET imaging research at Yale.

# Master's Thesis: Characterization of Neutron Response of Ionisation Chambers 

This is the repository of the Master's Thesis of Manuel Trigueros Galdon. The project is written in Python and is designed to run Monte Carlo N-Particle (MCNP) simulations for analyzing the behavior of different materials under various conditions.

## Prerequisites

To run the MCNP simulations in this project, you must have a valid license from Los Alamos National Laboratory. MCNP is a licensed software and its use is restricted to license holders only. Please visit the [official MCNP website](https://mcnp.lanl.gov/) for more information on how to obtain a license.

However, the analysis of the nuclear data can be performed using this application provided that the user has the necessary data files. Data files are included in this repository.
## Project Structure

The project is organized into several directories, each containing scripts for different types of simulations:

- `withCorrosion`: This directory contains scripts for running simulations of the ionization chamber with a corrosion layer. The simulations are designed to analyze the behavior of the chamber under various conditions, taking into account the effects of the corrosion layer.

- `withoutCorrosion`: This directory contains scripts for running simulations of a strontium 90 radiation source. The simulations are designed to analyze the behavior of the source under various conditions, without the presence of a corrosion layer.

- `Sr-90 source`: This directory contains scripts for running simulations of a simple cylinder to simulate a plastic A150 cylinder irradiated by a plane neutron source. The simulations are designed to analyze the behavior of the cylinder under various conditions.

## Getting Started

To get started with the project, you will need to have Python installed on your system. You can then clone the repository and install the required dependencies.

```bash
git clone https://github.com/mgaldon17/BEMP_Thesis.git
cd BEMP_Thesis
pip install -r requirements.txt
```

## Running the Simulations

To run the simulations, you can use the `run.py` script in the respective directory based on the type of simulation you want to run. This script sets up the MCNP simulations with the specified source and material, runs the simulations, and then analyzes the results.

```bash
python run.py
```

## Understanding the Results

The results of the simulations are analyzed and presented in a clear and understandable format. The analysis includes the calculation of various parameters such as the density of the solute, the percentage of the solute, and the type of particle. These parameters are then used to understand the behavior of the materials under the conditions of the simulation.

## Contributing

Contributions are welcome. Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

Please note that this is a general overview of the project. For more specific details, please refer to the individual scripts and their respective documentation.
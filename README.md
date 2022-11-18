SPyRender
=========

SPyRender is a package devoted to the generation of synthetic images for spaceborn instruments
based on SPICE geometry. It integrates a lightweight physically based offscreen renderer
with support for GPU-accelerated rendering. 

SPICE is an essential tool for scientists and engineers alike in the 
planetary science field for Solar System Geometry. Please visit the NAIF 
website for more details about SPICE.

![alt text](https://github.com/esaSPICEservice/spyrender/blob/master/SIM/ROSETTA_2015-10-21T07:03:42.90.PNG?raw=true) 
![alt text](https://github.com/esaSPICEservice/spyrender/blob/master/SIM/JUICE_2035-05-19T06:45:39.93.PNG?raw=true) 

Function and Purpose
--------------------

The generation of synthetic images is used in different steps of a space mission, from AOCS and GNC systems,
to Instrument Calibration and Data Analysis. SPyRender requires the user to specify 
few parameters regarding the observing camera, targets bodies and time of interest, and SPyRender
obtains the rest of the required geometric parameters from the kernel pool of the specified meta-kernel
to be loaded. 

SPyRender is developed and maintained by the [ESA SPICE Service (ESS)](https://spice.esac.esa.int).


Approach for SPyRender
----------------------

SPyRender can either be provided as a Service by ESS or it can be provided as a 
piece of software to be integrated in the given project SGS system. Configuration 
management and distribution of the software is discussed in the appropriate 
section of this document. Depending on the taken approach the relationships 
with other systems might change. What is described here assumes service providing 


Configuration file
------------------

The parameters to be specified in the configuration file are described hereafter:


Installation
------------

There is no need to install SPyRender. If you wish to use SPyRender, first download or clone the project. 
Then update the config file ``config.json`` with the parameters for your study case and run ``python spyrender.py``.


Requirements:
-------------

- [Python](https://www.python.org/) >= 3.6
- [numpy](https://numpy.org/) >= 1.8.0
- [matplotlib](https://matplotlib.org/) >= 3.5.0
- [spiceypy](https://github.com/AndrewAnnex/SpiceyPy/) >= 4.0.3
- [trimesh](https://trimsh.org/) >= 3.14.1
- [pyrender](https://github.com/mmatl/pyrender/) >= 0.1.45


How to Help
-----------

Feedback and new functionalities are always welcome, if you discover that a 
function is not 
working as expected or if you have a function that you believe can be of 
interest to other people please open an issue or contact [me](alfredo.escalantd.lopez@ext.esa.int).


Known Working Environments:
---------------------------

SPyRender is compatible with modern 64 bits versions of Linux and Mac. 
If you run into issues with your system please submit an issue with details. 

- OS: OS X, Linux
- CPU: 64bit
- Python 3.5
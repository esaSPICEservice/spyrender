SPyRender
=========

SPyRender is a package devoted to the generation of synthetic images for spaceborn instruments
based on SPICE geometry. It integrates a lightweight physically based offscreen renderer
with support for GPU-accelerated rendering. 

SPICE is an essential tool for scientists and engineers alike in the 
planetary science field for Solar System Geometry. Please visit the NAIF 
website for more details about SPICE.

![alt text](https://github.com/esaSPICEservice/spyrender/blob/master/SIM/ROSETTA_2015-10-21T07:03:43.80.PNG?raw=true) 
![alt text](https://github.com/esaSPICEservice/spyrender/blob/master/SIM/JUICE_2035-05-19T06:45:40.93.PNG?raw=true) 

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

- **Metakernel**: Path to the meta-kernel to load.
- **utc0**: Start date
- **utcf**: End date
- **tsamples**: Number of samples (number of images)
- **observer**: Name of observer body providing position of the camera focal point
- **camera**: Name of instrument as defined in the SPICE Instrument Kernel for which field of view and detector parameters will be extracted
- **camera frame** (optional): Reference frame of the camera, if left blank, SPyRender will try to obtain the instrument frame from the kernel pool 
- **yfov** (optional): Field of view reference angle, if left blank, SPyRender will try to obtain the reference angle from the kernel pool 
- **aspectratio** (optional): Ratio of Field of view cross angle to reference angle, if left blank, SPyRender will try to compute the aspect ratio from the kernel pool 
- **pxlines** (optional): Pixel lines, if left blank, SPyRender will try to obtain the pixel lines from the kernel pool 
- **pxsamples** (optional): Pixel samples, if left blank, SPyRender will try to obtain the pixel samples from the kernel pool 
- **targetsobj**: List specifying the path to the shape models (.OBJ format) of the different targets
- **targetsname**: List specifying the body name of the different targets
- **targetsframe**: List specifying the body fixed reference frame of the different targets
- **illumsource**: Name of the illumination source
- **lightfactor**: Float controlling the intensity of the illumination source
- **znear**: Float controlling the Near Clipping plane of the camera
- **bg**: RGBA color vector for the background
- **alpha**: If True, the background will not be rendered
- **smooth**: If True, the shading of faces will be smooth, if False, the shading of faces will be flat. As a rule of thumb, smooth should be set as True for ellipsoids and False for other bodies.
- **plot**: If True, it will plot each render image with Matplotlib
- **save**: If True, it will save each render image in the output directory
- **output**: Path to the output directory where to save the render images

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
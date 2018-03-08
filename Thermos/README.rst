*********************************************************************************************
                                       Thermos
*********************************************************************************************


This directory contains the following:  
  
1. __init__.py : which is an empty file present only to make Thermos a valid project.  
  
2. static : this directory contains the static things for the project like javascript and css files.  
  
3. templates : this directory contains the html pages for the project  
  
4. thermos.py : this is the view (controller as per MVC architecture) for the project  
  
------------------------------------------------------------------------------------------------  
                                IMPORTANT POINTS  
------------------------------------------------------------------------------------------------  
1) Rebuild a new virtualenv  
Using the appropriate Python version:  
  
virtualenv --python=/usr/bin/pythonX.Y /home/myusername/path/to/virtualenv  
or, with virtualenvwrappper  
  
mkvirtualenv --python=/usr/bin/pythonX.Y my-virtualenv-name  
  
2) Reinstall your packages  
  
pip install -r tmp/requirements.txt  # or path to your existing requirements.txt  

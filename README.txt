This project is the serve as a basic AI researcher assistant that researches topics that you give it.

This README file outlines the workings of the application, and the process taken to create it.


------------------------------------------PROCESS TAKEN------------------------------------------------

                                        STEP ONE: Setup/requirements

Initially, a virtual environment for this python project needed to be created. This was done using the command:
    python3 -m venv venv
The above command creates a virtual environment using venv, called venv. (hence "venv venv").

I then activated the virtual environment using the following command:
    source ./venv/bin/activate

I attempted to install the dependencies listed in requirements.txt, using the following command:
    pip3 install -r ./requirements.txt

This did not work, although python and pip were up-to-date. I worked around this by installing the dependencies
individually using the following commands:
    pip install wikipedia
    pip install anthropic
etc.


                                        STEP TWO: 

Created the prompt template that provides a structure for the conversation between the user and the AI system


                                        STEP THREE:


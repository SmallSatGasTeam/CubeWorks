# CubeWorks Documentation

CubeWorks is documented using Doxygen, a free and simple automatic documentation generator.  

## Building the Docs

The output directory is set to be ignored by git so the documentation is not committed to source control.  To build the CubeWorks documentation, do the following:

### Install Doxygen

To install Doxygen, simply run the following command from a linux shell:

`$ sudo apt install doxygen`

If you are using a Windows or MacOS system, you can either install the windows version as outlined in the Doxygen setup instructions (http://www.doxygen.nl/manual/install.html) or install the Windows Subsystem for Linux and run the command there. There is also Homebrew entry for Doxygen for Mac users.  

### Run Doxygen

Doxygen is already configured to build the documentation using the `Doxyfile` file included in the root directory of the project.  Simply use the following command:

`$ doxygen Doxyfile`

Doxygen will run and output the documentation in `GASPACS/docs/doxygen`.  To view the documentation as a web page, `cd` into `GASPACS/docs/doxygen/html` and run `index.html` or double click on `index.html` in your file browser.  Doxygen also generates LaTeX documents for the project.   

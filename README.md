# Automated AP analysis for cardiotoxicity testing on hiPSC-derived cardiac 3D microtissues

This workspace houses a collection of python script and sample data links that are published in Plos One 2023, entitled "Automated Data Analysis Pipeline for Cardiotoxicity Testing Using Optically Mapped hiPSC-derived 3D Cardiac Microtissues" by Arvin H. Soepriatna, Allison Navarrete-Welton, Tae Yun Kim, Mark C. Daley, Peter Bronk, Celinda M. Kofron, Ulrike Mende, Kareen L.K. Coulombe, Bum-Rak Choi. 

## Required Python Packages

This python script is provided as a Jupyter notebook so users can easily test and incorporate the algorithms into their own softwares. To run this python script, two main software should be installed, Jupyter notebook (https://jupyter.org/) and Anaconda python distribution (https://www.anaconda.com/products/distribution).

From the Anaconda Powershell prompt, please install following python packages; 
    numpy for numerical analysis,
    scipy for numerical analysis,
    pandas for data input and output,
    Dataset for reading the raw optical mapping data in the netCDF format,
    matplotlib for plotting,
    seaborn for additional visualization,
    cv2 for visualization and segmentation,
    sklearn for logistic and PCA analysis. 



To install these packages, use the following command.

    conda install 'package name here'


## Usage

1. Automated data analysis
To run the automated data analysis routines with a sample data, please download the script file 'Algorithms_Demo_Cardiotoxicity.ipynb'. Download a sample data set '2021-07-30-060.nc' from the link (https://doi.org/10.7910/DVN/YCPHZ9) under 'sample_data' subdirectory. The Juypter file has the python routines including thresholding, baseline correction using asymmetric least squares algorithm, measurements of risetime and repoliarization using moving average subtraction. The detailed descriptions of parameters and usage are provided in the routines. All other raw data of optical mapping are also available from the link (https://doi.org/10.7910/DVN/YCPHZ9)


2. Logistic Regression analysis
To run the logistic regression analysis, please download the script file 'LogisticRegression_CardiotoxicityAlgorithms.ipynb' to the main directory and all the necessary data files under the 'experiment_data' subdirectory. These data files contain 8 AP metrics and are in the CSV file format. The analysis script has two parts including a) experimentally obtained AP metrics changes under selective ion channel blockers and b) computer simulation results under selective ion channel blockade. Open 'LogisticRegression_CardiotoxicityAlgorithms.ipynb' from the Juypter program.


## Contributing

## History

This python packages and sample data were first uploaded on Dec 12th, 2022

## Credits
The software packages were originally written in Interactive Data languages (https://www.l3harrisgeospatial.com/) by Bum-Rak Choi and Taeyun Kim. This package in IDL is available at OMpro githup site (https://github.com/bumrak/OMPro). Allison Navarrete-Welton ported the IDL codes into python in 2022. 

## License

copyright © 2022, Bum-Rak Choi, Taeyun Kim, Allison Navarrete-Welton
 This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

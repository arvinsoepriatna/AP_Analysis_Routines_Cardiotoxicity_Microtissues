#python class to read Choi lab optical mapping data
# Copyright (C) 2015 Bum-Rak Choi and Taeyun Kim
#
# OMproData.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OMproData.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


# OM data structure
# netCDF 3.0 version
# DIMENSIONS array
#       d = [self.iChnX, self.iChnY, self.iChnXCam, self.iChnYCam, 
#            self.iNumChns, self.iNumChnsCam, self.iNumAuxChns]
# COMMENT 
#       string value of comments
# SCANINTERVAL
#       float value of frame interval in ms
# Data
#       variable name for actual raw data
#       16 bit signed integer 
#       Data[frame_ind, channel_ind] configuration
#       it has 10000 channels of CMOS camera + 2 stimulation logic channel
#       see an example of plotting raw data below
#       test_read_file()

# OMData class
#       reads and writes optical mapping data in the netCDF file format

import ctypes # import *
import numpy as np
from netCDF4 import Dataset 
import numpy as np
import matplotlib.pyplot as plt


       
class OMData:
   def __init__(self):
        self.date = np.zeros(6, dtype=np.int16)
        self.strFileNameBase = 'Simul-'
        self.strFilePath ='d:\\data\\'
        # creating a dummy data set
        self.iNumChns = 10007
        self.iNumChnsCam = 10000
        self.iChnX = 100
        self.iChnY = 100
        self.iChnXCam = 100
        self.iChnYCam = 100
        self.iNumAuxChns = 7
        self.iNumPixels = self.iNumChns - self.iNumAuxChns
        self.iNumFrames = 1024
        self.flag= np.ones(10007, dtype=np.float32)
        self.XYLocOfChn = np.zeros((1007,2), dtype=np.int16)
        self.fMinMax = np.zeros((10007,3), dtype=np.float32)
        self.comment = 'Start'
        self.fScanInt = 1.0
        self.t = np.arange(self.iNumFrames) * self.fScanInt
        self.data = np.zeros((self.iNumFrames, 10007), dtype=np.float32) #c type array
        # dummy data
        for i in range(self.iNumChns):
            self.data[:,i] = np.sin((self.t + i)/10.0)
        self.calc_MinMax()
        self.calc_XYLocOfChn()

   def calc_MinMax(self):
        self.fMinMax = np.zeros((self.iNumChns,3), dtype=np.float32)
        self.fMinMax[:,0] = np.amin(self.data, axis=0)
        self.fMinMax[:,1] = np.amax(self.data, axis=0)
        self.fMinMax[:,2] = self.fMinMax[:,1] - self.fMinMax[:,0]

   def calc_XYLocOfChn(self):
       ind = np.arange(self.iNumChns, dtype=np.int32)
       self.iXYLocChn = np.zeros((self.iNumChns, 2), dtype=np.int32)
       self.iXYLocChn[:,0] = np.mod(ind,self.iChnX)
       self.iXYLocChn[:,1] = np.floor(ind/self.iChnX)
   
   def read_data(self, filename):
        fid = Dataset(filename, "r")
        print(fid)
        self.date = fid.DATE
        self.comment = fid.COMMENT
        self.fScanInt = fid.SCANINTERVAL
        self.sDataType = fid.DATATYPE
        d = fid.DIMENSIONS
        self.iChnX = d[0]
        self.iChnY = d[1]
        self.iChnXCam = d[2]
        self.iChnYCam = d[3]
        self.iNumChns = d[4]
        self.iNumChnsCam = d[5]
        self.iNumAuxChns = d[6]
        self.iNumPixels = self.iNumChns - self.iNumAuxChns
        vm = fid.variables['Data']
        self.data = vm[:]
        self.iNumFrames = self.data.shape[0]
        fid.close()
        print('Data loaded calculating min max')
        self.t = np.arange(self.iNumFrames) * self.fScanInt / 1000.0 # ms
        self.calc_MinMax()
        self.calc_XYLocOfChn()
        print('Done')
        print('data type', self.data.dtype)
   def write_data(self, filename):
       fid = Dataset(filename, "w", format="NETCDF3_CLASSIC")
       fid.DATE=np.array(self.date, dtype=np.int16)
       d = [self.iChnX, self.iChnY, self.iChnXCam, self.iChnYCam, 
            self.iNumChns, self.iNumChnsCam, self.iNumAuxChns]#, self.iNumAuxChns]
       fid.COMMENT = self.comment
       fid.DIMENSIONS= np.array(d, dtype=np.int32)
       fid.createDimension('x', self.iNumChns)
       fid.createDimension('y', self.iNumFrames)
       fid.SCANINTERVAL = self.fScanInt
       fid.DATATYPE = self.sDataType
       if (self.data.dtype == 'float32') or (self.data.dtype == 'float64'):
           datatypestr = 'f4' # reducing to float 32
       else :
           datatypestr = 'i2' # signed integer
       vm = fid.createVariable('Data', datatypestr, ('y','x'))
       vm[:,:] = self.data
       fid.close()

   def get_ChnXY(self, x, y): # return a trace at location x, y
       iChn = self.iChnX * x + y # self.iXYLocChn[]
       res = np.float32(self.data[:, iChn])
       return res    
   def get_ChnXYN(self, x, y): # return a normalized trace
       iChn = self.iChnX * x + y # self.iXYLocChn[]
       return self.get_ChnN(iChn)
   def get_ChnN(self, iChn): # normalized trace
       nTrace = (np.float32(self.data[:,iChn]) - self.fMinMax[iChn, 0]) / self.fMinMax[iChn, 2]
       return nTrace
        
   def get_Img(self, iFrame):
       return np.reshape(self.data[iFrame, 0:self.iNumChnsCam], (self.iChnX, self.iChnY))
   def get_ImgN(self, iFrame):
       img = np.float32(self.data[iFrame, 0:self.iNumChnsCam])
       aMin = np.amin(img)
       aMax = np.amax(img)
       imgN = (img-aMin)/(aMax-aMin)
       return np.reshape(imgN, (self.iChnX, self.iChnY))
   def get_ImgIndN(self, iFrame):
       img = np.float32(self.data[iFrame, 0:self.iNumChnsCam])
       imgN = (img - self.fMinMax[0:self.iNumChnsCam,0]) / self.fMinMax[0:self.iNumChnsCam,2]
       return np.reshape(imgN, (self.iChnX, self.iChnY))
   def invert_data(self):
       self.data[:,0:self.iNumChnsCam] *= -1
       self.calc_MinMax()
   def invertSub_data(self):
       self.data[:,0:self.iNumChnsCam] *= -1
       self.data[:,0:self.iNumChnsCam] += 32767
       self.calc_MinMax()
       
def test_read_file():
    filename = 'D:/Data/SampleDataForPaper/2021-07-29-000.nc'
    oData = OMData()
    oData.read_data(filename)
    # show an image at 100
    plt.figure(0)
    aImg = oData.get_Img(100)
    plt.imshow(aImg)
    # channel location at 20, 20
    plt.figure(1)
    vm = oData.get_ChnXY(35,35)  
    # smooth window of 7
    kernel_size = 7
    kernel = np.ones(kernel_size) / kernel_size
    vmsmoothed = np.convolve(vm, kernel, mode='valid')
    # plot inverted vm
    plt.plot(-vmsmoothed)
    #filename = 'C:/Data/Sample/2020-06-19-003.nc'
    #oData.write_data(filename)
    return oData
       


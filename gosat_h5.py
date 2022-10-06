# coding:utf-8
import numpy as np
import sys
import h5py
import gdal
import geopandas
from shapely.geometry import Point
import argparse

__author__ = "TTY6335 https://github.com/TTY6335"
np.set_printoptions(suppress=True)

class show_info():
    hdf_file=None
    def __init__(self,h5_filename):
        self.hdf_file=h5_filename

    def satellite(self):
        return(self.hdf_file['Global']['metadata']['satelliteName'][()][0].decode("utf-8"))
    
    def sensor(self):
        return(self.hdf_file['Global']['metadata']['sensorName'][()][0].decode("utf-8"))

    def processingLevel(self):
        return(self.hdf_file['Global']['metadata']['operationLevel'][()][0].decode("utf-8"))

    def numScan(self):
        return(self.hdf_file['scanAttribute']['numScan'][()][0].decode("utf-8"))

    def scanID(self):
        return(self.hdf_file['scanAttribute']['scanID'][()][0].decode("utf-8"))

    def scanDirection(self):
        return(self.hdf_file['scanAttribute']['scanDirection'][()])

    def scanDuration(self):
        return(self.hdf_file['scanAttribute']['scanDuration'][()])

    def crossTrackObservationPoint(self):
        return(self.hdf_file['scanAttribute']['crossTrackObservationPoint'][()])

    def time(self):
        time_arr=[x.decode("utf-8") for x in self.hdf_file['scanAttribute']['time'][()]]
        return(time_arr)


class TANSOFTS_L2(show_info):
    def __init__(self,h5_filename,dataset_name):
        self.hdf_file=h5_filename
        self.dataset_name=dataset_name

        #メタデータを抽出
        self.metadata=show_info(self.hdf_file)

        #緯度経度情報を取り出す
        latitude=hdf_file['Data']['geolocation']['latitude'][()]
        longitude=hdf_file['Data']['geolocation']['longitude'][()]
        lat_lon_arr=np.column_stack((longitude,latitude))
    
        mid_key=find_key(input_file,dataset_name)
        targetdata=hdf_file['Data'][mid_key][dataset_name][()]

        #単位を取り出す
        unit=str(hdf_file['Data'][mid_key][dataset_name].attrs['unit'][()][0].decode("utf-8"))
        #longNameを取り出す
        longName=str(hdf_file['Data'][mid_key][dataset_name].attrs['longName'][()][0].decode("utf-8"))


        #二次元データ(Profileデータか)チェック
        #1次元の場合
        if(targetdata.ndim ==1):
        #GeoDataFrame用に整形
            d = {dataset_name: targetdata,
                'unit':[unit]*len(targetdata),
                'longName':[longName]*len(targetdata),
                'geometry': [Point(x) for x in lat_lon_arr],
                'time':self.metadata.time()
        }
        #2次元の場合
        if(targetdata.ndim== 2):

            lat_lon_arr=np.repeat(lat_lon_arr,targetdata.shape[1], axis=0)
            pressure=hdf_file['Data'][mid_key]['pressure'][()] 
    
            time_list=[]
            [time_list.extend([x]*targetdata.shape[1]) for x in self.metadata.time()]
    
            d = {dataset_name: targetdata.flatten(),
                    'pressure': pressure.flatten(),
                    'unit':[unit]*targetdata.shape[0]*targetdata.shape[1],
                    'longName':[longName]*targetdata.shape[0]*targetdata.shape[1],
                    'time':time_list,
                    'geometry': [Point(x) for x in lat_lon_arr]}

        self.gdf = geopandas.GeoDataFrame(d, crs="EPSG:4326")

    def gdf(self):
        return(gdf)

    def writeout(self,out_filename):
        if out_filename is None:
            print('outfile IS EMPTY.')
            exit(1);
        self.gdf.to_file(driver = 'GeoJSON', filename= out_filename)
        return(None)

def get_args():
    # 準備
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputfile", type=str)
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--outfile", type=str)

    # 結果を受ける
    args = parser.parse_args()

    return(args)

#Dataと、出力したいdatasetの間の階層のdataset名を取得する。
def find_key(input_file,dataset_name):

    flag=False
    for key_1st in list(hdf_file['Data'].keys()):
        for key_2st in list(hdf_file['Data'][key_1st].keys()):
            if(key_2st==dataset_name):
                flag=True
                break
        if(flag==True):
            break

    if(flag==False):
        print('%s IS MISSING.' % dataset_name)
        print('SELECT FROM BELOW.')
        for key_1st in list(hdf_file['Data'].keys()):
            for key_2st in list(hdf_file['Data'][key_1st].keys()):
                print(key_2st)
        exit(1);

    return(key_1st)

if __name__ == '__main__':

    args = get_args()
#入力するファイルの情報#
    #ファイル名
    input_file=args.inputfile
    #バンド名
    dataset_name=args.dataset
    #出力ファイル名
    output_file=args.outfile

    try:
        hdf_file = h5py.File(input_file,'r')
    except:
        print('%s IS MISSING.' % input_file)
        exit(1);
	

    metadata=show_info(hdf_file)
    print('SATELLITE: %s' % metadata.satellite())
    print('SENSOR: %s' % metadata.sensor())
    print('PROCESSING LEVEL: %s' % metadata.processingLevel())

    if(metadata.satellite()!='GOSAT'):
        print('THIS FILE IS NOT GOSAT')
        exit(1);

    if(metadata.sensor()!='TANSO-FTS'):
        print('THIS FILE IS NOT GOSAT TANSO-FTS')
        exit(1);

    if(metadata.processingLevel()!='L2'):
        print('THIS FILE IS NOT PROCESSING LEVEL L2')
        exit(1);

    tanso_fts=TANSOFTS_L2(hdf_file,dataset_name)
    tanso_fts.writeout(output_file)

##CLOSE HDF FILE
    hdf_file=None


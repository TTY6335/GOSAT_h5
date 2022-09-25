# coding:utf-8
import numpy as np
import sys
import h5py
import gdal
import geopandas
from shapely.geometry import Point
import argparse

__author__ = "TTY6335 https://github.com/TTY6335"

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

def show_metadata(hdf_file):
    print('Satellite Name: '+hdf_file['Global']['metadata']['satelliteName'][()][0].decode("utf-8"))
    print('Sensor Name: '+hdf_file['Global']['metadata']['sensorName'][()][0].decode("utf-8"))
    print('Processing Level: '+hdf_file['Global']['metadata']['operationLevel'][()][0].decode("utf-8"))


if __name__ == '__main__':

    args = get_args()
#入力するファイルの情報#
    #ファイル名
    input_file=args.inputfile
    #バンド名
    dataset_name=args.dataset

#出力ファイル名
#	output_file=sys.argv[3]

    try:
        hdf_file = h5py.File(input_file,'r')
    except:
        print('%s IS MISSING.' % input_file)
        exit(1);
	

    show_metadata(hdf_file)
    latitude=hdf_file['Data']['geolocation']['latitude'][()]
    longitude=hdf_file['Data']['geolocation']['longitude'][()]
    lat_lon_list=list(zip(longitude,latitude))

    mid_key=find_key(input_file,dataset_name)

    targetdata=hdf_file['Data'][mid_key][dataset_name][()]
    unit=str(hdf_file['Data'][mid_key][dataset_name].attrs['unit'][()][0].decode("utf-8"))
    longName=str(hdf_file['Data'][mid_key][dataset_name].attrs['longName'][()][0].decode("utf-8"))
    d = {dataset_name: targetdata,
            'unit':[unit]*len(targetdata),
            'longName':[longName]*len(targetdata),
            'geometry': [Point(x) for x in lat_lon_list]}
    gdf = geopandas.GeoDataFrame(d, crs="EPSG:4326")
    gdf.to_file(driver = 'GeoJSON', filename= "result.geojson")

##CLOSE HDF FILE
    hdf_file=None


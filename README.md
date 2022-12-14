# GOSAT_h5

## このプログラム??
GOSAT のL2 TANSO-FTSセンサのL2,L3データをgeopandasで出力、またはGeoJSONファイルで出力するプログラムです。(対応するセンサ、処理レベルは追加予定)  
現在、GOSAT TANSO-FTSセンサ L2 TIRL, SWIRLに対応しています。

## 使い方
### L2  
python gosat_h5.py --inputfile=GOSATH5FILE.h5 --dataset=dataframe --outfile=out.geojson  
### L3
python gosat_h5.py --inputfile=GOSATH5FILE.h5 --dataset=dataframe --outfile=out.geotiff  

## 出力形式
### L2  
#### TIRLデータの場合
物理量と緯度経度の他に、単位、観測時刻、各プロファイルにおける気圧を出力します。
#### SWIRデータの場合  
物理量と緯度経度の他に、単位、観測時刻を出力します。  

### L3  
GeoTIFFにして物理量を出力します。無効値、単位、正式名をメタデータに付して出力します。

## 参考文献  
[地球観測データ利用ハンドブック（GOSAT/いぶき）](https://data2.gosat.nies.go.jp/doc/GOSAT_HB_J_1stEdition_for_HP.pdf)  
[NIES GOSAT TANSO-FTS SWIR レベル 2 プロダクトフォーマット説明書](https://data2.gosat.nies.go.jp/doc/documents/GOSAT_ProductDescription_21_FTSSWIRL2_V3.10_ja.pdf)  
[NIES GOSAT TANSO-FTS TIR レベル 2 プロダクトフォーマット説明書](https://data2.gosat.nies.go.jp/GosatDataArchiveService/doc/GU/GOSAT_ProductDescription_22_FTSTIRL2_V2.31_ja.pdf)

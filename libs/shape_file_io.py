# encoding: utf-8
"""
@version: 3.6
@author: mas
@file: shape_file_io.py
@time: 2020/6/13 11:14
"""
from osgeo import gdal, osr,ogr
from shapely import geometry


class GDAL_shp_Data(object):
    def __init__(self, shp_path):
        self.shp_path = shp_path
        self.shp_file_create()


    def shp_file_create(self):
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
        ogr.RegisterAll()
        # 注册驱动，打开测试文件和图层
        driver = ogr.GetDriverByName("ESRI Shapefile")
        # shp_file_path = SHP_FILE_PATH

        # 打开输出文件及图层
        # 输出模板shp 包含待写入的字段信息
        self.outds = driver.CreateDataSource(self.shp_path)
        # 创建空间参考
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)
        # 创建图层
        self.out_layer = self.outds.CreateLayer("out_polygon", srs, ogr.wkbPolygon)
        field_name = ogr.FieldDefn("置信度", ogr.OFTReal)
        self.out_layer.CreateField(field_name)
        field_name = ogr.FieldDefn("序号", ogr.OFTInteger)
        self.out_layer.CreateField(field_name)

    def set_shapefile_data(self,polygons,scores):
        for i in range(len(scores)):
            wkt = polygons[i].wkt            # 创建wkt文本点
            temp_geom=ogr.CreateGeometryFromWkt(wkt)
            feature = ogr.Feature(self.out_layer.GetLayerDefn()) # 创建特征
            feature.SetField("序号", i)
            feature.SetField("置信度", scores[i])
            feature.SetGeometry(temp_geom)
            self.out_layer.CreateFeature(feature)
        self.finish_io()

    def finish_io(self):
        del self.outds




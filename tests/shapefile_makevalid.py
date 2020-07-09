from osgeo import ogr, gdal, osr
import makevalid
import shapely.wkt


shp_path = "../data/result.shp"
out_path = "../data/out.shp"

def make_valid(shp_path):
    ds = ogr.Open(shp_path)
    if ds == None:
        print("打开文件%s失败", shp_path)
    iLayerCount = ds.GetLayerCount()  # 获取该数据源中的图层个数，一般shp数据图层只有一个，如果是mdb、dxf等图层就会有多个
    print(f"shp文件中共包含 {iLayerCount} 个图层")
    oLayer = ds.GetLayerByIndex(0)
    if oLayer == None:
        print("获取第%d个图层失败!\n", 0)

    feature_count = oLayer.GetFeatureCount(0)
    print(f"shp 中共有 {feature_count} 个多边形")

    out_shp = GDAL_shp_Data(out_path)
    valid_poly_list = []
    for i in range(0, feature_count):
        fea = oLayer.GetFeature(i)
        poly = fea.GetGeometryRef()
        if poly.IsValid() == False:
            print(f"feature index {i} 。。。。。。。。。。。。。{fea}。。。。。。。。。。。。。。。。。不合法！")
            poly_wkt = poly.ExportToWkt()
            poly_ly = shapely.wkt.loads(poly_wkt)
            valid_poly = makevalid.make_geom_valid(poly_ly)
            valid_poly_list.append(valid_poly)
        else:
            valid_poly_list.append(shapely.wkt.loads(poly.ExportToWkt()))
    out_shp.set_shapefile_data(valid_poly_list)


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
        self.out_layer = self.outds.CreateLayer("out_polygon", srs, ogr.wkbMultiPolygon)

    def set_shapefile_data(self,polygons):
        for polygon in polygons:
            wkt = polygon.wkt            # 创建wkt文本点
            temp_geom=ogr.CreateGeometryFromWkt(wkt)
            feature = ogr.Feature(self.out_layer.GetLayerDefn()) # 创建特征
            feature.SetGeometry(temp_geom)
            self.out_layer.CreateFeature(feature)
        self.finish_io()

    def finish_io(self):
        del self.outds

if __name__ == '__main__':
    make_valid(shp_path)
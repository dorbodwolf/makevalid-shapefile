def generate_tif_patch_in_shp(cfg, tif_dic):
    '''

    :param cfg: 工程配置相关参数
    :param tif_dic: 影像路径字典
    :return:
    '''

    shp_path = config.shp_path
    out_dir = config.output_folder

    # 1. 读取矢量shp数据
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = ogr.Open(shp_path, 1)
    if ds == None:
        print("打开文件%s失败", shp_path)
    iLayerCount = ds.GetLayerCount()  # 获取该数据源中的图层个数，一般shp数据图层只有一个，如果是mdb、dxf等图层就会有多个
    print(f"shp文件中共包含 {iLayerCount} 个图层")
    oLayer = ds.GetLayerByIndex(0)
    if oLayer == None:
        print("获取第%d个图层失败!\n", 0)
    oDefn = oLayer.GetLayerDefn()  # 获取图层中的属性表表头并输出
    iFieldCount = oDefn.GetFieldCount()
    for i in range(iFieldCount):
        oField = oDefn.GetFieldDefn(i)
        print("%s: %s(%d.%d)" % (
            oField.GetNameRef(), oField.GetFieldTypeName(oField.GetType()), oField.GetWidth(),
            oField.GetPrecision()))
    prosrs = oLayer.GetSpatialRef()  # 获取影像空间参考

    # 遍历所以要素
    # 2. 开始逐条提取
    feature_count = oLayer.GetFeatureCount(0)
    print(f"shp 中共有 {feature_count} 个多边形")
    feature = oLayer.GetNextFeature()
    # 记录可能存在问题的feature记录
    out_txt_file = open(osp.join(cfg.output_folder,"log.txt"), 'w')  # 以可写方式打开
    feature_index = 0
    while feature:
		geom = feature.GetGeometryRef()
		centroid_point_gdal = geom.Centroid()
		# 获取经度
		lat = centroid_point_gdal.GetY()
		# 获取纬度
		lon = centroid_point_gdal.GetX()
		# 经纬度转图像坐标
		# 获取feature对应的影像
		img_base_name = feature.GetFieldAsString(cfg.tif_field_name_in_shp)
		feature_fid = feature.GetFID()


		feature.Destroy()
		feature = oLayer.GetNextFeature()
		print(f"Processing feature index {feature_index} / {feature_count}  ...")
		feature_index += 1
    ds.Destroy()
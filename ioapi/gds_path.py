import ioapi.DataBlock_pb2 as DataBlock_pb2
import ioapi.GDS_data_service as GDS_data_service

def get_file_list(path):
    service = GDS_data_service.service
    # 获得指定目录下的所有文件
    status, response = service.getFileList(path)
    MappingResult = DataBlock_pb2.MapResult()
    file_list = []
    if status == 200:
        if MappingResult is not None:
            # Protobuf的解析
            MappingResult.ParseFromString(response)
            results = MappingResult.resultMap
            # 遍历指定目录
            for name_size_pair in results.items():
                if (name_size_pair[1] != 'D'):
                    file_list.append(name_size_pair[0])
    return file_list

def get_all_dir(path,all_path):
    # 初始化GDS客户端
    service = GDS_data_service.service
    # 获得指定目录下的所有文件
    status, response = service.getFileList(path)
    MappingResult = DataBlock_pb2.MapResult()
    if status == 200:
        if MappingResult is not None:
            # Protobuf的解析
            MappingResult.ParseFromString(response)
            results = MappingResult.resultMap
            # 遍历指定目录
            for name_size_pair in results.items():
                if (name_size_pair[1] == 'D'):
                    all_path.append(name_size_pair[0])
                    path1 = '%s%s%s' % (path, "/" , name_size_pair[0])
                    if(path1[0:1] == "/"):
                        path1 = path1[1:]
                    if(path1[0:1] == "/"):
                        path1 = path1[1:]
                    get_all_dir(path1,all_path)
                    print(name_size_pair[0])



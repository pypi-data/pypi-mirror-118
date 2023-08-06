# yyx_tools
项目开发过程中常用的一些开发工具，减少自己的重复代码量。


##安装
```
pip install yyx_tools
```


##使用
```
import yyx_tools as yt
```


##API
```
yt.file.save(dump_path, content, keep_ori) # 将str/np.array保存到指定文件中

yt.list.rm_elem(input_list, elem) # 检查elem是否存在于input_list中，如果存在则删除

yt.video.info(mp4_path) # 返回mp4信息，fps, total frames, image width, image height

yt.checkdir(dir_path) # 检查dir_path是否存在，如果不存在则创建

yt.load_yaml(yaml_path) # load yaml 并将其结构化和打印
```
# DatasetDownload

行为识别数据库的数据下载脚本
(一直下载一直在改 
dataDownload目录下有三个版本的

## dataact

主要是用了youtube_dl 和 bypy两个库 感谢

大致思路是在vps上下载到本地 然后上传到百度云 然后再由百度云拉回来

因此使用前需要首先安装依赖 requirements.txt
然后执行bypy info 授权百度云

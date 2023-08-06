# 数据集处理工具包
- 处理 COCO, VOC 格式的数据集
- 包含数据集互转、切分、检查

# 数据集格式说明

## VOC
VOC  
  |  
  |---------Annotations  
                |-------xxx.xml  
  |  
  |---------ImageSets  
                |  
                |-------Main    
                         |-------trainval.txt  
  |  
  |---------JPEGImages  
                |-------xxx.jpg
  |  
  |---------labels.txt

## COCO
COCO
  |  
  |---------Annotations  
                |-------train.json
  |  
  |---------JPEGImages  
                |  
                |-------train  
                         |-------xxx.jpg

# 使用方法
- pip 安装
> pip install cspdataset
- 命令行式使用
> datatools COMMAND
- 参数说明
> usage: datatools.py [-h] --form {coco,COCO,VOC,voc} --data_dir DATA_DIR  
                    [--split]  
                    [--division_ratio DIVISION_RATIO [DIVISION_RATIO ...]]  
                    [--transform] [--output_transform OUTPUT_TRANSFORM]  
                    [--check] [--output_check OUTPUT_CHECK]  
                    [--labelfile LABELFILE] [--eva EVA]


>tools for voc/coco dataset   
optional arguments:    
  -h, --help                             show this help message and exit    
  --form {coco,COCO,VOC,voc}             the form of the dataset  
  --data_dir DATA_DIR                    the dir of the dataset  
  --split                                Set a switch to split  
  --division_ratio DIVISION_RATIO [DIVISION_RATIO ...] data segmentation ratio  
  --transform                            Set a switch to transform  
  --output_transform OUTPUT_TRANSFORM    dir for output  
  --check                                Set a switch to check  
  --output_check OUTPUT_CHECK            dir for output  
  --labelfile LABELFILE                  the labels.txt from the platform  


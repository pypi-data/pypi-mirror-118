# -*- coding: utf-8 -*-
from nn_sdk import *
'''
    前言: 
        当前支持开发语言c/c++,python,java
        当前支持推理引擎tensorflow(v1,v2) onnxruntime tensorrt 注:tensorrt 7,8测试通过(建议8), 目前tensorrt只支持linux系统
        当前支持多子图,支持图多输入多输出, 支持pb [tensorflow 1,2] , ckpt [tensorflow] , trt [tensorrt]
        模型加密参考test_aes.py,目前支持tensorflow 1 pb模型 , onnx模型 , tensorrt模型加密
        推荐环境ubuntu16 ubuntu18  ubuntu20 centos7 centos8 windows系列
        python (test_py.py) , c语言 (test.c) , java语言包 (nn_sdk.java)
        使用过程中遇到问题或者有建议可加qq group: 759163831
        更多使用参见: https://github.com/ssbuild
'''
'''
    python 推理demo
    config 字段介绍:
        aes: 加密参考test_aes.py,目前支持tensorflow 1 pb模型 , onnx模型 , tensorrt模型加密
        engine: 推理引擎 0: tensorflow , 1: onnx , 2: tensorrt
        log_level: 日志类型 0 fatal , 2 error , 4 info , 8 debug
        model_type: tensorflow 模型类型, 0 pb format , 1 ckpt format
        ConfigProto: tensorflow 显卡配置
        device_id: GPU id
        engine_version: 推理引擎主版本 tf 0,1  tensorrt 7 或者 8 , 需正确配置
        graph: 多子图配置 
            node: 例子: tensorflow 1 input_ids:0 ,  tensorflow 2: input_ids , onnx: input_ids
            data_type: 节点的类型根据模型配置，支持 int int64 long longlong float double 
            shape:  形状大小
'''
config = {
    "model_dir": r'E:/root/model.ckpt',
    "aes":{
        "use":False,
        "key":bytes([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]),
        "iv":bytes([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]),
    },
    "log_level": 4,
    'engine':0,
    "device_id": 0,
    'tf':{
        "ConfigProto": {
            "log_device_placement": False,
            "allow_soft_placement": True,
            "gpu_options": {
                "allow_growth": True
            },
        },
        "engine_version": 1,
        "model_type": 1,
    },
    'onnx':{
        "engine_version": 1,
    },
    'trt':{
        "engine_version": 8,
        'enable_graph': 0,
    },
    "graph": [
        {
            "input": [
                {"node":"input_ids:0", "data_type":"int64", "shape":[1, 256]},
                {"node":"input_mask:0", "data_type":"int64", "shape":[1, 256]}
            ],
            "output": [
                {"node":"pred_ids:0", "data_type":"int64", "shape":[1, 256]},
            ],
        }
    ]}

seq_length = 256
input_ids = [[1] * seq_length]
input_mask = [[1] * seq_length]
sdk_inf = csdk_object(config)
if sdk_inf.valid():
    net_stage = 0
    ret, out = sdk_inf.process(net_stage, input_ids,input_mask)
    print(ret)
    print(out)
    sdk_inf.close()
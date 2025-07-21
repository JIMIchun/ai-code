- 安装依赖：
```
pip3 install -r requirements.txt
```
- 运行项目(后端/数据库)：
```
python3 run.py
```

- 病历生成测试：
```
python3 test.py
```

- 语音测试访问：
```
http://127.0.0.1:5000/voice-input
```

- 使用语音功能需要安装ffmpeg:
```
sudo apt-get install ffmpeg   #linux
```

- 项目目录结构：
flask_demo
├── app
│   ├── models  # 数据库模型
│   └── routes  # 路由
│   └── services  # 业务逻辑
│   └── templates  # 页面模板
├── run.py  # 运行项目
├── test.py  # 病历生成测试
├── requirements.txt  # 依赖
├── README.md  # 说明文档
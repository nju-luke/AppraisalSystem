build

创建dockerfile

```sh
# Base Images
## 从天池基础镜像构建
FROM registry.cn-shanghai.aliyuncs.com/tcc-public/python:3

## 把当前文件夹里的文件构建到镜像的根目录下
ADD . /

## 指定默认工作目录为根目录（需要把run.sh和生成的结果文件都放在该文件夹下，提交后才能运行）
WORKDIR /

## 镜像启动后统一执行 sh run.sh
CMD ["sh", "run.sh"]
```

创建image

```sh
 docker image build -t trip_luke/test_submit:1.0 .	# 生成一个image
```

运行

```sh
docker run -it 374750278fbe	# ---> 生成运行的container
docker ps	# ---> 正在运行的container
docker container stop 52d7c5b8ca84 
```





导出导入

```sh
 docker save -o test.tar trip_luke/test_submit:latest
 docker load -i test.tar
```



image命令：

```sh
docker image ls
docker image prune
docker image rm a4cc999cf2aa

docker push test_submit:latest
```


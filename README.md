# AppraisalSystem

## mytest主要涉及用户注册机权限管理的测试
包括内容
1. 导航分流页
2. 有权限才可访问的页面
3. 注册页（包括管理员注册）—— 管理员注册时分配权限 （当前权限为系统自带的权限）
4. 登录才可访问的页面
5. 未登录、登录、有权限三中情况下对用户的状态判断
6. 用户密码修改

## plots中包含主要逻辑
包含内容
1. 默认登录页（未登录的访问都跳转到登录页）

2. 登录后使用默认配置：有团队权限的可访问团队数据；没有团队权限的跳转到个人详情页

   

todo
- [ ]  定时任务
- [ ]  详情页列表的区分显示



docker执行步骤：

1. docker pull yhyhbo/appraisal

2. 启动container
   
    ```shell script
    docker run --name app -d -p 1324:1324 -i yhyhbo/appraisal
    ```
    
3. 修改settings

    两种方法：

    - 进入container内部

      ```sh
      docker exec -it app bash
      vi settings.py
      # 修改其中的数据库配置信息，NAME表示数据库，DRIVER不用改
      ```

    - 拷贝到本地修改

      ```sh
      # 复制settings到本地
      docker cp app:/home/AppraisalSystem/settings.py .
      
      # 修改settings.py中的数据库配置
      
      # 上传到数据库
      docker cp ./settings.py app:/home/AppraisalSystem/settings.py
      ```

4. 进入服务器启动服务

    ```sh
    docker exec -it app bash
    ```

    分为2个步骤：

    - 初始化，只需要做一次（后面可直接跳过）

      ```sh
      python manage.py makemigrations
      python manage.py migrate
      ```

    - 启动服务

      ```sh
      python manage.py runserver 0.0.0.0:1324
      ```

访问地址：localhost:1324

创建superuser
```shell script
python manage.py createsuperuser
```

批量创建用户
```shell script
python create_user.py <文件路径>

#文件使用\t作为分隔符
#文件包含两列, 保持第一行为：username	password
```


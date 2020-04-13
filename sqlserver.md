[toc]

# 使用docker创建sqlserver服务

## 拉取sqlserver的image

```sh
docker pull exoplatform/sqlserver
```

## 启动sqlserver服务
```sh
docker run --privileged -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=Do8gjas07gaS1" -e "SQLSERVER_DATABASE=testdb" -e "SQLSERVER_USER=root" -e "SQLSERVER_PASSWORD=Do8gjas07gaS1" -p 1433:1433 --name=MSSQL exoplatform/sqlserver
```

## 启动sqlserver client
```sh
docker exec -it MSSQL /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Do8gjas07gaS1
# 此处的MSSQL表示上一步启动的container, 可使用docker start/stop MSSQL 来启动和关闭
```

## 进入MSSQL对应的container

```sh
docker exec -it MSSQL /bin/bash
```

## 权限配置

```sh
Use ecology
GO
Create User root For Login sa with Default_Schema= [dbo];
go
use ecology
go
EXEC sp_addrolemember "db_ddladmin", N"root"
go

EXEC ecology..sp_addsrvrolemember @loginame = N"root", @rolename = N"dbcreator"
GO
```

# django 连接sqlserver

## 安装插件

```sh
# https://github.com/ESSolutions/django-mssql-backend
pip install pyodbc 
pip install django-mssql-backend
```

## 配置

```python
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE' : 'sql_server.pyodbc',
        'NAME' : 'ecology',
        'HOST' : 'localhost',
        'PORT' : 1433,
        'USER' : 'root',
        'PASSWORD' : 'Do8gjas07gaS1',
        'OPTIONS': {
            # 'DRIVER': '{SQL Server}'	# 注意，此处的配置可能跟下一条的错误有关系
        },

    }
}
```



## django 连接sql server报错 Error: ('IM002', '[IM002] [Microsoft][ODBC 驱动程序管理器] 未发现数据源名称并且未指定默认驱动程序 (0) (SQLDriverConnect)')

可能原因，没有具体的驱动。

（通过调试模式，发现实际使用的驱动是ODBC Driver 13 for SQL Server，与options中设置的driver无关）

可在[此处](https://docs.microsoft.com/zh-cn/sql/connect/odbc/windows/release-notes-odbc-sql-server-windows?view=sql-server-ver15#13)下载调试中看到的具体驱动，下载安装到电脑上。



# dataGrip中导入数据

1. 使用import Data From File查看DDL，不直接导入，直接导入可能报错；然后在consol中执行DDL，创建表
2. 再使用import导入对应创建的表中



# docker创建mysql服务

## 拉取镜像

```sh
docker pull mysql
```

## mysql启动
```sh
docker run --name longk -e "MYSQL_ROOT_PASSWORD=Do8gjas07gaS1" -p 3306:3306 mysql
# 注意添加端口，否则不能连接
```

## 使用启动mysql的container连接mysql
```sh
docker exec -it longk bash
mysql -pDo8gjas07gaS1
```

## django 不能连接，报错"Access denied for user "root"@"172.17.0.1" (using password: YES)")

```sql
ALTER USER "root"@"%" IDENTIFIED WITH mysql_native_password BY "Do8gjas07gaS1"; 

update user set authentication_string=password("Do8gjas07gaS1") where user="root"；

ALTER USER 'root'@'%' IDENTIFIED BY 'Do8gjas07gaS1'
```


# django session
> django 可通过session保存当前登录的信息
```python
request.session['args'] = {'key1':'value1'}
```





# docker 间的访问

1. 通过link

   ```
   docker run -itd --name MSSQL -p 1433:1433 mssql
   docker run -itd --name app --link MSSQL:mssql yhyhbo/appraisal
   # 在第二个docker中指定第一个docker的link，则可以通过：后面的alise ping通前一个docker
   ```

   

2. 通过内建网络

   ```sh
   docker run -it --network=my_net2 --name=bbox1 busybox
   docker run -it --network=my_net2 --name=bbox2 busybox
   ```

   







linux中安装driver后报错：sqlalchemy.exc.DBAPIError: (pyodbc.Error) ('01000', "[01000] [unixODBC][Driver Manager]Can't open lib 'SQL Server' : file not found (0) (SQLDriverConnect)")

1. 查看配置：odbcinst -j

```
	unixODBC 2.3.1
	DRIVERS............: /etc/odbcinst.ini
	SYSTEM DATA SOURCES: /etc/odbc.ini
	FILE DATA SOURCES..: /etc/ODBCDataSources
	USER DATA SOURCES..: /root/.odbc.ini
	SQLULEN Size.......: 8
	SQLLEN Size........: 8
	SQLSETPOSIROW Size.: 8
```

2. 查看odbcinst.ini中的配置，并将驱动复制一份，修改命名：

   cat /etc/odbcinst.ini

```
	[SQL Server]
	Description=Microsoft ODBC Driver 13 for SQL Server
	Driver=/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.0.so.1.0
	UsageCount=1

	[ODBC Driver 13 for SQL Server]
	Description=Microsoft ODBC Driver 13 for SQL Server
	Driver=/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.0.so.1.0
	UsageCount=1
```
# Base Images
# FROM tmp4
FROM conda/miniconda3-centos7

MAINTAINER nju.hyhb@gmail.com

RUN echo y|yum install curl

RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo_bak \
    && echo y|curl http://mirrors.163.com/.help/CentOS7-Base-163.repo > /etc/yum.repos.d/CentOS-Base.repo \
    && yum clean all \
    && yum makecache

RUN curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo \
   && echo y|yum update \
   && echo y|ACCEPT_EULA=Y yum install -y msodbcsql-13.0.1.0-1 mssql-tools-14.0.2.0-1 \
   && echo y|yum install unixODBC-utf16-devel \
   && ln -sfn /opt/mssql-tools/bin/sqlcmd-13.0.1.0 /usr/bin/sqlcmd  \
   && ln -sfn /opt/mssql-tools/bin/bcp-13.0.1.0 /usr/bin/bcp \
   && echo y|yum install gcc-c++ \
   && echo y|yum install python-devel

RUN yum install -y git

RUN mkdir -p /home

RUN pip install  pyodbc Django==3.0.4 django-mssql-backend plotly==4.5.4 SQLAlchemy==1.3.10 pandas==0.24.2 numpy==1.16.4
#-i https://pypi.tuna.tsinghua.edu.cn/simple

## copy files
ADD . /home/AppraisalSystem

## setting the working directory
WORKDIR /home/AppraisalSystem


CMD ["bash"]

### execute the commands after the container start
# CMD  ["python", "manage.py", "runserver", "1324"]
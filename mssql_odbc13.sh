echo y|yum install curl
curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo
echo y|yum update
echo y|ACCEPT_EULA=Y yum install -y msodbcsql-13.0.1.0-1 mssql-tools-14.0.2.0-1
echo y|yum install unixODBC-utf16-devel
ln -sfn /opt/mssql-tools/bin/sqlcmd-13.0.1.0 /usr/bin/sqlcmd 
ln -sfn /opt/mssql-tools/bin/bcp-13.0.1.0 /usr/bin/bcp
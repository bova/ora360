## ORA 360 Readme

## Install Dependencies
  
* pip install cx_Oracle    
* pip install jinja2 
* pip install pandas
* pip install setuptools
* pip install plotly
* pip install -U kaleido


## Пользователь в базе данных

```SQL
grant select on sys.V_$diag_Alert_Ext to zabbix;
```
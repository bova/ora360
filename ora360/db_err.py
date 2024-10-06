import cx_Oracle
import ora360.conf

ORA_ERR_SQL = """
select Trunc(a.Originating_Timestamp, 'MI') as Originating_Timestamp,
       a.Host_Id,
       a.Module_Id,
       a.Message_Text
  from V$diag_Alert_Ext a
 where a.Originating_Timestamp > (SYSDATE - INTERVAL '7' Day)
   and Regexp_Like(a.Message_Text, '^.*ORA-[[:digit:]]{5}.*')
"""


class OraErrRow:
    originating_timestamp = ''
    host_id = ''
    module_id = ''
    message_text = ''

    def __init__(self, cur_result):
        self.originating_timestamp = cur_result[0]
        self.host_id = cur_result[1]
        self.module_id = cur_result[2]
        self.message_text = cur_result[3]


class OraErr:
    def __init__(self, cfg):
        self.cfg = ora360.conf.AppConf()
        self.cfg = cfg
        self.conn_url = self.get_conn_url()
        self.conn = ''

    def get_conn_url(self):
        connection_url = self.cfg.db.host + ':' + self.cfg.db.port + '/' + self.cfg.db.service_name
        return connection_url

    def get_connection(self):
        self.conn = cx_Oracle.connect(self.cfg.db.user, self.cfg.db.password, self.conn_url)

    def execute_query(self):
        cur = self.conn.cursor()
        for row in cur.execute('select * from user_tables'):
            print(row)

    def get_ora_errors(self):
        ora_err_list = []
        self.get_connection()
        cur = self.conn.cursor()
        for row in cur.execute(ORA_ERR_SQL):
            ora_err = OraErrRow(row)
            ora_err_list.append(ora_err)
        return ora_err_list


if __name__ == '__main__':
    conf = ora360.conf.AppConf()
    conf.parse(ora360.conf.CONF_FILE_CANDIDATES)
    conn = OraErr(conf)
    print(conn.get_ora_errors())

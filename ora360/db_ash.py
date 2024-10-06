import cx_Oracle
import ora360.conf
import pandas
import plotly.express as px
import base64

ASH_SQL2 = """
select Trunc(Sample_Time, 'MI') as Sample_Time,
       Wait_On,
       Round(count(*) * 10 / 60, 1) as Cnt
  from (select Sample_Time,
               case
                 when Session_State = 'ON CPU' then
                  'CPU'
                 when Session_State = 'WAITING' and Wait_Class = 'User I/O' then
                  'User I/O'
                 when Session_State = 'WAITING' and Wait_Class != 'User I/O' then
                  'WAIT'
               end as Wait_On
          from Dba_Hist_Active_Sess_History
         where Sample_Time > (SYSDATE - INTERVAL '7' Day) and Sample_Time < (SYSDATE - INTERVAL '1' Hour))
 group by Trunc(Sample_Time, 'MI'), Wait_On
 order by Sample_Time
"""

ASH_SQL = """
select Sample_Time,
       Nvl(Cpu, 0) as Cpu,
       Nvl(User_Io, 0) as User_Io,
       Nvl(Wait, 0) as Wait
  from (select Trunc(Sample_Time, 'HH24') as Sample_Time,
               Wait_On,
               Round(count(*) * 10 / (60*60), 1) as Cnt
          from (select Sample_Time,
                       case
                         when Session_State = 'ON CPU' then
                          'CPU'
                         when Session_State = 'WAITING' and
                              Wait_Class = 'User I/O' then
                          'User I/O'
                         when Session_State = 'WAITING' and
                              Wait_Class != 'User I/O' then
                          'WAIT'
                       end as Wait_On
                  from Dba_Hist_Active_Sess_History
                 where Sample_Time > (SYSDATE - INTERVAL '7' Day))
         group by Trunc(Sample_Time, 'HH24'), Wait_On)
Pivot(sum(Cnt)
   for Wait_On in('CPU' Cpu, 'User I/O' User_Io, 'WAIT' Wait))
"""

class ASH:
    def __init__(self, cfg):
        self.cfg = ora360.conf.AppConf()
        self.cfg = cfg
        self.conn_url = self.get_conn_url()
        self.conn = ''
        self.get_connection()

    def get_conn_url(self):
        connection_url = self.cfg.db.host + ':' + self.cfg.db.port + '/' + self.cfg.db.service_name
        return connection_url

    def get_connection(self):
        self.conn = cx_Oracle.connect(self.cfg.db.user, self.cfg.db.password, self.conn_url)

    def execute_query(self):
        cur = self.conn.cursor()
        for row in cur.execute('select * from user_tables'):
            print(row)

    def get_ash(self):
        ash_list= []
        cur = self.conn.cursor()
        for row in cur.execute(ASH_SQL):
            ash = row
            ash_list.append(ash)
        return ash_list

    def get_ash_graph(self):
        data = self.get_ash()
        df = pandas.DataFrame(data)
        df.columns = ['Sample_Time', 'CPU', 'User I/O', 'WAIT']

        # plotly
        fig = px.area(df,
                      x='Sample_Time',
                      y=['CPU', 'User I/O', 'WAIT'],
                      color_discrete_sequence=["green", "blue", "orange"],
                      title="ASH report")
        fig.update_xaxes(title_text='Дата')
        fig.update_yaxes(title_text='Кол-во сессий')
        fig.update_layout(legend_title_text='Ожидание')

        # Show plot
        # fig.show()
        # res = fig.to_html()
        img = fig.to_image(format='svg', width=1200, height=600)
        img_base64 = base64.b64encode(img)
        img_base64_str = img_base64.decode('ascii')
        return img_base64_str


if __name__ == '__main__':
    conf = ora360.conf.AppConf()
    conf.parse(ora360.conf.CONF_FILE_CANDIDATES)
    conn = ASH(conf)
    data = conn.get_ash()
    df = pandas.DataFrame(data)
    print(df)
    df.columns = ['Sample_Time', 'CPU', 'User I/O', 'WAIT']
    print(df)
    df_cumsum = pandas.concat([df['Sample_Time'], df[['CPU', 'User I/O', 'WAIT']].cumsum(axis=1)], axis=1)
    print(df_cumsum)
    # plotly
    color_discrete_map = {'CPU': 'green', 'User I/O': 'blue', 'WAIT': 'orange'}
    # fig = px.area(df, x=0, y=2, color=1, color_discrete_map=color_discrete_map, labels=labels, pattern_shape=1)
    fig = px.area(df, x='Sample_Time', y=['CPU','User I/O','WAIT'], color_discrete_sequence=["green", "blue", "orange"])
    fig.update_xaxes(title_text='Дата')
    fig.update_yaxes(title_text='Кол-во сессий')
    fig.update_layout(legend_title_text='Ожидание')
    # Show plot
    fig.show()




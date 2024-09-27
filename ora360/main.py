from ora360 import conf, db, markup
from datetime import datetime
import os


def get_file_name_plus_tod(file_name):
    file_base_name, file_ext = os.path.splitext(file_name)
    now = datetime.now()
    tod = now.strftime("%Y%m%d")
    new_file_name = file_base_name + '_' + tod + file_ext
    return new_file_name


def save_report_to_file(file_name, file_content):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(file_content)


if __name__ == '__main__':
    cfg = conf.AppConf()
    cfg.parse(conf.CONF_FILE_CANDIDATES)
    conn = db.DB(cfg)
    html = markup.HTML()
    # mailer = mail.Mail(cfg)

    backup_summary_list = conn.get_backup_summary()
    backup_detail_dict = conn.get_backup_details()
    msg_content = html.render(backup_summary_list, backup_detail_dict)
    # mailer.add_attachment_from_string(get_file_name_plus_tod('ora360.html'), msg_content)
    # mailer.send(msg_content)
    save_report_to_file(get_file_name_plus_tod('c:\\temp\\ora360.html'), msg_content)
    print(msg_content)


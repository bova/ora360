from jinja2 import Environment, PackageLoader


class HTML:
    def __init__(self):
        file_loader = PackageLoader('ora360', 'templates')
        env = Environment(loader=file_loader)
        self.template = env.get_template('report.html')

    def render(self, backup_summary_list, backup_detail_dict, ash_graph, ora_err_list):
        return self.template.render(backup_summary_list=backup_summary_list, backup_detail_dict=backup_detail_dict, ash_graph=ash_graph, ora_err_list=ora_err_list)


if __name__ == '__main__':
    html = HTML()

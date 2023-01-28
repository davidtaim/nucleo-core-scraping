from datetime import datetime


class Logger:
    @staticmethod
    def print_log(log: str) -> None:
        f = open('logs.txt', 'a')
        log = '[' + datetime.now().strftime('%d-%m-%Y - %H:%M:%S') + ']: ' + log + '\n'
        f.write(log)
        f.close()

    @staticmethod
    def print_links_to_check(link) -> None:
        f = open('links.txt', 'a')
        log = '[' + datetime.now().strftime('%d-%m-%Y - %H:%M:%S') + ']: ' + link + '\n'
        f.write(log)
        f.close()

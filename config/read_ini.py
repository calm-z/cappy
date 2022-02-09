# 读取ini配置文件的模块
import configparser


# 读取配置文件中的内容
def ReadIni(section, option):
    conf = configparser.ConfigParser()
    conf.read("/Users/purehol/PycharmProjects/cappy/config/conf.ini")
    value = conf.get(section, option)
    return value


if __name__ == '__main__':
    print(ReadIni('TEST_SERVER', 'url'))

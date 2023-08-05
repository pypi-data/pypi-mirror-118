import os
import zipfile


def en_to_cn():
    filename = idle_backup()
    import os
    os.rename(filename, 'idle_en')
    backup_idle_files('idle_cn.zip')


def un_en_to_cn():
    backup_idle_files('idle_en')
    print('解除成功')


def backup_idle_files(zip_name):
    import shutil
    try:
        shutil.rmtree('../../idlelib')
        shutil.rmtree('./idlelib')
    except OSError:
        pass
    z = zipfile.ZipFile(zip_name, 'r')
    z.extractall('idlelib')
    shutil.copytree('./idlelib', '../../idlelib')
    print('成功')


def zip_path(input_path, output_name):
    z = zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, filenames in os.walk(input_path):
        for filename in filenames:
            z.write(os.path.join(dir_path, filename))


def idle_backup():
    import datetime
    import shutil
    try:
        shutil.rmtree('./idlelib')
    except OSError:
        pass
    shutil.copytree('../../idlelib', './idlelib')
    zip_name = "idle_old_%s" % str(datetime.datetime.now())
    zip_name = zip_name.replace(':', '_')
    zip_name = zip_name.replace(' ', '_')
    zip_path('idlelib', r'./%s' % zip_name)
    print('备份成功！')
    return zip_name


def backup():
    f = []
    for value1 in os.walk('./'):
        if value1:
            for value2 in value1:
                if 'idle_old_' in value2:
                    f.append(value1)
    print('已备份的IDLE时间:')
    for value1 in f:
        print(value1)
    v = input('请输入要还原的版本号（时间）：')
    while v not in f:
        v = input('输入错误')
    backup_idle_files(v)


if __name__ == '__main__':
    pass
else:
    x = []
    y = 1
    for a in os.walk(r'./'):
        if a:
            for b in a:
                if 'idle_old_' in b:
                    x.append(1)
                if 'idle_cn' not in b:
                    y = 0
    if y:
        t = '未备份,请输入idle_cn.idle_backup()进行备份'
        if x:
            t = '已备份'
        print('''欢迎使用idle中文版！
        您的IDLE%s!
        还原IDLE，请输入idle_cn.backup()
        解除汉化，请输入idle_cn.un_en_to_cn()''' % t)
    else:
        print('''欢迎使用idle中文版！
        idle未汉化，输入idle_cn.en_to_cn()汉化。''')

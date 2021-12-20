import os
import chardet

# 指定根目录
root_path = r"./dp"

# 指定排除目录
exclude_path_list = [r"./build", ]
# 指定需要更改的文件后缀
suffix_list = [r".cpp", r".c", r".java", r".dart", ]
count = 0
def check_file_suffix(file, suffix_list):
    for p in suffix_list:
        if file.endswith(p):
            return True
    return False

def check_path_exclude(path, exclude_path_list):
    for p in exclude_path_list:
        if path.startswith(p):
            return True
    return False

def main():
    global count
    for path, subdirs, files in os.walk(root_path):
        if check_path_exclude(path, exclude_path_list):
            continue
        for name in files:
            file = os.path.join(path, name)
            if check_file_suffix(file, suffix_list):
                print(file)
                with open(file, 'rb') as f:
                    c = chardet.detect(f.read())
                    s = open(file, mode='r', encoding=c['encoding']).read()  # UTF-8 with BOM
                    open(file, mode='w', encoding='utf-8').write(s)  # UTF-8 without BOM
                    count += 1
    print("共", count, "个文件，转换完毕")


if __name__ == '__main__':
    main()
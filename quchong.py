
import hashlib
import os


# 指定根目录
root_path = r"e:\aa"
# 指定排除目录
exclude_path_list = [r"./build", ]
# 指定需要更改的文件后缀
suffix_list = [r".cpp", r".c", r".java",  ]
suffix_list = [r".dart", ]
count = 0
fileMap={}

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

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def main():
    global count
    for path, subdirs, files in os.walk(root_path):
        if check_path_exclude(path, exclude_path_list):
            continue
        for name in files:
            file = os.path.join(path, name)
            if check_file_suffix(file, suffix_list):
                xmd5 = (GetFileMd5(file))
                count += 1
                if xmd5 in fileMap.keys():
                    #os.system("rm " +fileMap[fileMap])
                    print("\nrm " +fileMap[xmd5])
                else:
                    pass
                fileMap[xmd5] = file


if __name__ == '__main__':
    main()
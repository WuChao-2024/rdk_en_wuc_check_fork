import os

def search_string_in_files(directory, target_strings):
    cnt = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line_no, line in enumerate(lines, start=1):
                        for target in target_strings:
                            if target in line:
                                cnt += 1
                                print("\033[32m" + f'{cnt}: Found "{target}" in file: \"{filepath}\", line {line_no}' + "\033[0m")
                                print(line.replace(target, '\033[31m{}\033[0m'.format(target)))
                                break  # 如果找到一个目标字符串，则可以跳过当前行的其他目标搜索

with open("test.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    # 定义要搜索的目标字符串
    for line in lines:
        print(line[:-1])
        target_strings = [line[:-1]]
        # 开始在./doc目录下搜索
        search_string_in_files('./docs', target_strings)
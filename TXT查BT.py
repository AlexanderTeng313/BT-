import os

def print_file_info(file_path):
    """打印文件基本信息"""
    try:
        file_size = os.path.getsize(file_path)
        print("\n文件信息:")
        print(f"路径: {file_path}")
        print(f"大小: {file_size / 1024 / 1024:.2f} MB")
    except Exception as e:
        print(f"获取文件信息时出错: {str(e)}")

def normalize_string(s):
    """将字符串标准化，把空格和点号都转换为同一个分隔符"""
    return s.lower().replace(' ', '.').replace('..', '.')

def search_in_file(file_path, keyword, previous_results=None):
    try:
        found_count = 0
        results = []
        normalized_keyword = normalize_string(keyword)

        # 确定搜索源
        if previous_results:
            search_lines = previous_results
            source_desc = "上次搜索结果"
        else:
            search_lines = open(file_path, 'r', encoding='utf-8', errors='ignore')
            source_desc = f"文件 '{file_path}'"

        print(f"\n在{source_desc}中搜索关键字 '{keyword}' 的结果：\n")

        for line in search_lines:
            normalized_line = normalize_string(line.strip() if isinstance(line, str) else line)
            if normalized_keyword in normalized_line:
                found_count += 1
                print(line.strip())
                results.append(line.strip())

        if not previous_results:
            search_lines.close()

        if found_count == 0:
            print(f"未找到包含关键字 '{keyword}' 的结果")
            print("\n建议：")
            print("1. 检查关键字拼写是否正确")
            print("2. 尝试使用更短的关键字")
            return []
        else:
            print(f"\n共找到 {found_count} 个种子")
            return results

    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return []
    except Exception as e:
        print(f"发生错误：{str(e)}")
        return []

def main():
    print("BT文件搜索工具")
    print("提示：搜索不区分大小写")
    print("提示：输入 'n' 开始新搜索，输入 'q' 退出")
    
    # 让用户输入文件路径
    while True:
        file_path = input("\n请输入种子数据文件路径: ").strip('"')  # 去除可能复制来的引号
        if os.path.exists(file_path):
            break
        print(f"\n错误：文件 {file_path} 不存在！请重新输入")

    print_file_info(file_path)
    previous_results = None

    while True:
        try:
            keyword = input("\n请输入要搜索的关键字: ")

            if keyword.lower() == 'q':
                print("程序已退出")
                break
            elif keyword.lower() == 'n':
                previous_results = None
                print("\n开始新的搜索...")
                continue

            if keyword:
                previous_results = search_in_file(file_path, keyword, previous_results)
            else:
                print("请输入有效的关键字！")

        except KeyboardInterrupt:
            print("\n程序已被用户中断")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            break

if __name__ == "__main__":
    main()
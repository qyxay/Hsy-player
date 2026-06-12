import os
import re

root_dir = r"D:\HuaweiMoveData\Users\Qyxay\Desktop\Hu-Shiyi-Divine-Realm-of-the-Other-World-main"
folder_order = ["one", "two", "three", "four", "five", "six"]
output_txt = os.path.join(root_dir, "全剧集清单.txt")

# 自定义优先级：阴阳行者篇权重0，其余篇章权重1，保证它排在同文件夹最前
def get_chapter_priority(chapter_name):
    if chapter_name == "阴阳行者篇":
        return 0
    return 1

def sort_episodes_in_folder(file_list):
    def sort_key(filename):
        match = re.search(r"(.*?篇) 第(\d+)集", filename)
        if match:
            chap = match.group(1)
            ep = int(match.group(2))
            # 排序元组：(篇章优先级, 篇章名称, 集数)
            return (get_chapter_priority(chap), chap, ep)
        # 无标准篇章集数格式的文件放文件夹末尾
        return (999, "zzzz未知篇章", 999999)
    return sorted(file_list, key=sort_key)

final_lines = []
print("===== 按 one~six 顺序分层收集m4a文件 =====")

for folder in folder_order:
    folder_path = os.path.join(root_dir, folder)
    print(f"正在处理文件夹：{folder}")
    if not os.path.isdir(folder_path):
        print(f"警告：{folder} 文件夹不存在，跳过")
        continue
    
    folder_audio = []
    # 递归读取当前文件夹所有子目录m4a
    for dirpath, _, filenames in os.walk(folder_path):
        for fname in filenames:
            if fname.lower().endswith(".m4a"):
                folder_audio.append(fname)
    
    # 当前文件夹内排序：阴阳行者篇置顶，同篇章集数升序
    sorted_folder_audio = sort_episodes_in_folder(folder_audio)
    final_lines.extend(sorted_folder_audio)

# 写入txt
with open(output_txt, "w", encoding="utf-8") as f:
    for line in final_lines:
        f.write(f"{line}\n")

print(f"✅ 全部完成！总采集 {len(final_lines)} 个音频文件")
print(f"规则：先one文件夹（阴阳行者篇置顶）→two→three→four→five→six，每个文件夹内篇章分组、集数升序")
print(f"清单路径：{output_txt}")
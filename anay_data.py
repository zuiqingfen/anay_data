import os
from collections import Counter
import heapq

def distribute_words_by_hash(input_file, output_dir):
    
    os.makedirs(output_dir, exist_ok=True)
    # 创建100个文件句柄
    file_handles = {}
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                word = line.strip()
                if not word:
                    continue
                
                # 计算hash值并取前两位
                hash_value = hash(word)
                hash_group = abs(hash_value) % 100  # 取模确保范围在0-99
                
                # 如果该分组的文件句柄还不存在，则创建
                if hash_group not in file_handles:
                    output_file = os.path.join(output_dir, f"group_{hash_group:02d}.txt")
                    file_handles[hash_group] = open(output_file, 'w', encoding='utf-8')
                
                # 将词写入相应的文件
                file_handles[hash_group].write(f"{word}\n")
    
    except Exception as e:
        print(f"处理文件时发生错误: {e}")
    
    finally:
        # 关闭所有文件句柄
        for handle in file_handles.values():
            handle.close()


def find_top_words_in_files(input_dir, output_dir, top_n=10):
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有分组文件
    group_files = [f for f in os.listdir(input_dir) if f.startswith('group_') and f.endswith('.txt')]
    
    for group_file in group_files:
        # 构建完整的输入文件路径
        input_file_path = os.path.join(input_dir, group_file)
        
        # 使用Counter统计词频
        word_counts = Counter()
        
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                word = line.strip()
                if word:
                    word_counts[word] += 1
        
        top_words = heapq.nlargest(top_n, word_counts.items(), key=lambda x: x[1])
        
        # 构建输出文件路径
        output_file_path = os.path.join(output_dir, f"top_{group_file}")
        
        # 将结果写入输出文件
        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            for word, count in top_words:
                out_file.write(f"{word}\t{count}\n")
        
        print(f"已处理文件 {group_file}，找出了{len(top_words)}个高频词")


def find_global_top_words(temp_dir, top_n=10):
   
    global_counter = Counter()
    
    # 遍历temp_dir目录下的所有文件
    for filename in os.listdir(temp_dir):
        if filename.startswith('top_group_') and filename.endswith('.txt'):
            file_path = os.path.join(temp_dir, filename)
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split('\t')
                    if len(parts) == 2:
                        word, count = parts
                        # 累计词频
                        global_counter[word] += int(count)
    
    # 找出频率最高的top_n个词
    top_words = heapq.nlargest(top_n, global_counter.items(), key=lambda x: x[1])
    
    # 返回结果
    return top_words




if __name__ == "__main__":
    # input_file = "random_words_100MB.txt"
    # output_dir = "word_groups"
    # distribute_words_by_hash(input_file, output_dir)
    
    # input_dir = "word_groups"  # 上一步生成的分组文件目录
    # output_dir = "temp_data"   # 存放高频词的目录
    # find_top_words_in_files(input_dir, output_dir)
    
    # 调用函数并打印结果
    temp_dir = "temp_data"
    top_words = find_global_top_words(temp_dir)

    print("出现频率最高的10个词:")
    for i, (word, count) in enumerate(top_words, 1):
        print(f"{i}. {word}: {count}次")

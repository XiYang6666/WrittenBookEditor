import argparse
import os
import shutil
import zipfile
from pathlib import Path


def extract_font_resources(jar_path, output_dir):
    """
    从 JAR 文件中提取字体资源

    参数:
        jar_path (str): 输入的 JAR 文件路径
        output_dir (str): 输出目录路径
    """
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(jar_path, "r") as jar:
            # 遍历 JAR 文件中的所有文件
            for file_info in jar.infolist():
                file_path = file_info.filename

                # 处理 assets/minecraft/font/ 下的文件
                if file_path.startswith("assets/minecraft/font/"):
                    # 构建目标路径
                    relative_path = os.path.relpath(file_path, "assets/minecraft/font")
                    dest_path = os.path.join(output_dir, "./", relative_path)

                    # 确保目录存在
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                    # 提取文件
                    with jar.open(file_path) as source, open(dest_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                    print(f"提取: {file_path} -> {dest_path}")

                # 处理 assets/minecraft/textures/font/ 下的文件
                elif file_path.startswith("assets/minecraft/textures/font/"):
                    # 构建目标路径
                    relative_path = os.path.relpath(file_path, "assets/minecraft/textures/font")
                    dest_path = os.path.join(output_dir, "./textures/", relative_path)

                    # 确保目录存在
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                    # 提取文件
                    with jar.open(file_path) as source, open(dest_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                    print(f"提取: {file_path} -> {dest_path}")

    except zipfile.BadZipFile:
        print(f"错误: {jar_path} 不是有效的 ZIP/JAR 文件")
    except Exception as e:
        print(f"提取过程中发生错误: {str(e)}")


def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="从 JAR 文件中提取 Minecraft 字体资源")
    parser.add_argument("jar_file", help="输入的 JAR 文件路径")
    parser.add_argument("-o", "--output", default="./", help="输出目录 (默认为当前目录)")

    args = parser.parse_args()

    # 调用提取函数
    print(f"开始从 {args.jar_file} 提取字体资源...")
    extract_font_resources(args.jar_file, args.output)
    print("提取完成!")


if __name__ == "__main__":
    main()

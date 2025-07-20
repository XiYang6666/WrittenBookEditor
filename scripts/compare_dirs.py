import argparse
import hashlib
import os
import sys
from typing import List, Optional, Tuple


def calculate_file_hash(filepath: str, block_size: int = 65536) -> str:
    """计算文件的MD5哈希值"""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def find_first_existing_file(source_dirs: List[str], relative_path: str) -> Optional[Tuple[str, str]]:
    """在源目录列表中查找第一个存在的文件，返回(文件路径, 哈希值)"""
    for src_dir in source_dirs:
        src_path = os.path.join(src_dir, relative_path)
        if os.path.exists(src_path):
            return (src_path, calculate_file_hash(src_path))
    return None


def compare_directories(source_dirs: List[str], target_dir: str, auto_clean: bool = False) -> Tuple[List[str], int, int]:
    """比较源目录和目标目录中的文件"""
    differences = []
    files_processed = 0
    files_removed = 0
    target_files = set()

    # 首先处理目标目录中的文件
    for root, _, files in os.walk(target_dir):
        for filename in files:
            files_processed += 1
            target_path = os.path.join(root, filename)
            relative_path = os.path.relpath(target_path, target_dir)
            target_files.add(relative_path)

            target_hash = calculate_file_hash(target_path)
            src_file = find_first_existing_file(source_dirs, relative_path)

            if src_file is None:
                differences.append(f"Missing in sources: {relative_path}")
                continue

            src_path, src_hash = src_file
            if target_hash != src_hash:
                differences.append(f"Content differs: {relative_path} (src: {src_path})")
            elif auto_clean:
                os.remove(target_path)
                files_removed += 1
                differences.append(f"Removed (same content): {relative_path}")

    # 然后检查源目录中有但目标目录中没有的文件
    for src_dir in source_dirs:
        for root, _, files in os.walk(src_dir):
            for filename in files:
                src_path = os.path.join(root, filename)
                relative_path = os.path.relpath(src_path, src_dir)

                if relative_path not in target_files:
                    differences.append(f"Missing in target: {relative_path} (src: {src_path})")

    return differences, files_processed, files_removed


def validate_directories(dirs: List[str]) -> List[str]:
    """验证目录是否存在并返回有效的目录列表"""
    valid_dirs = []
    for dir_path in dirs:
        if os.path.isdir(dir_path):
            valid_dirs.append(dir_path)
        else:
            print(f"Warning: Directory does not exist and will be ignored: {dir_path}")
    return valid_dirs


def main():
    parser = argparse.ArgumentParser(
        description="Compare files between multiple source directories and a target directory using hash comparison"
    )
    parser.add_argument("--sources", nargs="+", required=True, help="List of source directories (in order of priority)")
    parser.add_argument("--target", required=True, help="Target directory to compare against")
    parser.add_argument(
        "--clean", action="store_true", help="Automatically remove files in target that have identical content to source files"
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed comparison results")

    args = parser.parse_args()

    valid_sources = validate_directories(args.sources)
    if not valid_sources:
        print("Error: No valid source directories provided")
        sys.exit(1)

    if not os.path.isdir(args.target):
        print(f"Error: Target directory does not exist: {args.target}")
        sys.exit(1)

    print(f"Comparing sources: {valid_sources} with target: {args.target}")
    if args.clean:
        print("Auto-clean mode enabled - identical files will be removed from target")

    differences, processed, removed = compare_directories(valid_sources, args.target, args.clean)

    print("\nComparison results:")
    if args.verbose or len(differences) <= 20:
        for diff in differences:
            print(diff)
    else:
        print(f"Found {len(differences)} differences (use --verbose to see all)")
        for diff in differences[:10]:
            print(diff)
        if len(differences) > 10:
            print(f"... and {len(differences) - 10} more differences")

    print("\nStatistics:")
    print(f"Total files processed: {processed}")
    print(f"Total differences found: {len(differences)}")
    if args.clean:
        print(f"Files removed from target: {removed}")


if __name__ == "__main__":
    main()

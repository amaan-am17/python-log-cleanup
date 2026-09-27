from pathlib import Path
from datetime import datetime, timedelta
import sys


def get_mode():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "--dry-run"


def get_max_age_minutes():
    if len(sys.argv) > 2:
        try:
            max_age_minutes = int(sys.argv[2])
        except ValueError:
            print("Invalid age. Please provide a number of minutes.")
            sys.exit(1)

        if max_age_minutes < 0:
            print("Invalid age. Minutes cannot be negative.")
            sys.exit(1)

        return max_age_minutes

    return 5


def find_log_files(log_directory):
    return list(log_directory.glob("*.log"))



def get_file_age(log_file):
    modified_time = datetime.fromtimestamp(log_file.stat().st_mtime)
    age = datetime.now() - modified_time
    return modified_time, age


def analyze_log_file(log_file):
    content = log_file.read_text(encoding="utf-16")
    lines = content.splitlines()

    info_count = 0
    warning_count = 0
    error_count = 0

    for line in lines:
        if "INFO" in line:
            info_count += 1
        elif "WARNING" in line:
            warning_count += 1
        elif "ERROR" in line:
            error_count += 1

    return info_count, warning_count, error_count


def cleanup_log(log_file, age, max_age, dry_run):
    if age > max_age:
        print("OLD LOG:", log_file)

        if dry_run:
            print("DRY RUN: would delete", log_file)
            return False

        log_file.unlink()
        print("DELETED:", log_file)
        return True

    return False


def print_summary(total_files, deleted_count, total_info, total_warning, total_error, dry_run):
    print()
    print("=== Cleanup Summary ===")
    print("Files scanned:", total_files)
    print("Files deleted:", deleted_count)
    print("INFO entries:", total_info)
    print("WARNING entries:", total_warning)
    print("ERROR entries:", total_error)

    if dry_run:
        print("Mode: DRY RUN")
    else:
        print("Mode: CLEAN")


def main():
    mode = get_mode()

    if mode == "--dry-run":
        dry_run = True
    elif mode == "--clean":
        dry_run = False
    else:
        print("Invalid mode. Use --dry-run or --clean.")
        sys.exit(1)

    max_age_minutes = get_max_age_minutes()
    max_age = timedelta(minutes=max_age_minutes)

    log_directory = Path.cwd() / "logs"

    if not log_directory.exists():
        print("Log directory not found:", log_directory)
        sys.exit(1)

    print(log_directory)
    print(log_directory.exists())

    log_files = find_log_files(log_directory)

    if not log_files:
        print("No log files found.")
        sys.exit(0)

    print("Log files found:", len(log_files))

    deleted_count = 0
    total_info = 0
    total_warning = 0
    total_error = 0
    for log_file in log_files:
        modified_time, age = get_file_age(log_file)
        info_count, warning_count, error_count = analyze_log_file(log_file)
        total_info += info_count
        total_warning += warning_count
        total_error += error_count
        print("INFO:", info_count)
        print("WARNING:", warning_count)
        print("ERROR:", error_count)
        print("File:", log_file)
        print("Modified:", modified_time)
        print("Age:", age)

        if cleanup_log(log_file, age, max_age, dry_run):
            deleted_count += 1

    print_summary(
        len(log_files),
        deleted_count,
        total_info,
        total_warning,
        total_error,
        dry_run
    )

if __name__ == "__main__":
    main()
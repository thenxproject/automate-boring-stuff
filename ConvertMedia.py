#!/usr/bin/env python3
import os
import shutil
import re
import resource
import psutil


file_extensions = (".mkv", ".m2ts", ".avi")


def limit_memory(max_memory_gb: int = 48):
    max_memory_bytes = max_memory_gb * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (max_memory_bytes, max_memory_bytes * 2))


def limit_cpu(number_of_cores: int = int(os.cpu_count() * .75)):
    number_of_cores_to_use = list(range(number_of_cores))
    process = psutil.Process(os.getpid())
    process.cpu_affinity(number_of_cores_to_use)


def get_files_in_directory(path: str) -> list[str]:
    return sorted([file for file in os.listdir(os.path.expanduser(path)) if file.endswith(file_extensions)])


def get_sub_directories(path: str) -> list[str]:
    return sorted([folder for folder in os.listdir(os.path.expanduser(path)) if not folder.startswith(".")])


def convert_file(path: str, file_name: str) -> None:
    input_file = f"{path}/{file_name}"
    for extension in list(file_extensions):
        file_name = file_name.replace(extension, '.mp4')
    output_file = f"{path}/{file_name}"
    print(f"Converting {re.search(r".*(Movies|TV).*", path).group(1)}: {input_file.replace(f"{path}/", '')} > {file_name}")
    os.system(f"""HandBrakeCLI -i "{input_file}" -o "{output_file}" --audio-lang-list eng,jpn,und --subtitle none --preset "HQ 1080p30 Surround" -v 0 > /dev/null 2>&1""")

    # Moves the original file to a temp backup directory
    os.system(f'''mv "{input_file}" "/mnt/Temp/Backup/{input_file.replace(f"{path}/", '')}" > /dev/null 2>&1''')


def convert_movies() -> None:
    letters = get_sub_directories("/mnt/Movies2")
    for letter in letters:
        movies = get_sub_directories(f"/mnt/Movies2/{letter}")
        for movie in movies:
            files = get_files_in_directory(f"/mnt/Movies2/{letter}/{movie}")
            for file in files:
                convert_file(f"/mnt/Movies2/{letter}/{movie}", file)


def convert_tv() -> None:
    shows = get_sub_directories("/mnt/TV2")
    for show in shows:
        seasons = get_sub_directories(f"/mnt/TV2/{show}")
        for season in seasons:
            episodes = get_files_in_directory(f"/mnt/TV2/{show}/{season}")
            for episode in episodes:
                convert_file(f"/mnt/TV2/{show}/{season}", episode)


# Entrypoint for the running of the application
if __name__ == '__main__':
    limit_memory()
    limit_cpu()
    convert_movies()
    convert_tv()

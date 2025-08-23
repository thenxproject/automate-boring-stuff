#!/usr/bin/env python3
import os


def get_files_in_directory(path: str) -> list[str]:
    return [file for file in os.listdir(os.path.expanduser(path)) if file.endswith(".mkv")]


def get_sub_directories(path: str) -> list[str]:
    return [folder for folder in os.listdir(os.path.expanduser(path)) if not folder.startswith(".")]



def convert_file(path: str, file_name: str) -> None:
    input_file = f"{path}/{file_name}"
    output_file = f"{path}/{file_name.replace('.mkv', '.mp4')}"
    os.system(f"""HandBrakeCLI -i "{input_file}" -o "{output_file}" --preset "HQ 1080p30 Surround" -v 0""")

    # Moves the original file to a temp backup directory
    os.rename(input_file, f"/mnt/Temp/Backup/{file_name}")


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
    convert_movies()
    #convert_tv()

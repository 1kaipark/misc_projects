import os

dir = input("directory to cleanse: \n").strip()
files_root = os.listdir(dir)
for file in files_root:
    if file == '.DS_Store':
        os.remove(os.path.join(dir, file))
        print(f"deleted {os.path.join(dir, file)}")

subdirs = next(os.walk(dir))[1]
for subdir in subdirs:
    files_sd = os.listdir(subdir)
    for file in files_sd:
        if file == '.DS_Store':
            os.remove(os.path.join(dir, subdir, file))
            print(f"deleted {os.path.join(dir, subdir, file)}")
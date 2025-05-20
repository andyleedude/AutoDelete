import os
import send2trash
from concurrent.futures import ThreadPoolExecutor

folder_lists = \
    [fr"C:\Users\Andy Li\AppData\Local\Temp",
     fr"C:\Users\Andy Li\AppData\Local\NVIDIA\DXCache",
     fr"C:\Users\Andy Li\AppData\Local\D3DSCache",
     fr"C:\Users\Andy Li\AppData\Roaming\WeMod\Partitions\ads",
     fr"C:\Users\Andy Li\AppData\Local\CrashDumps"
     ]


def try_send_to_trash(file_path):
    if not os.access(file_path, os.W_OK):
        print(f"Skipped {file_path} (no write permission)")
        return

    try:
        if os.path.isfile(file_path) or os.path.isdir(file_path):
            send2trash.send2trash(file_path)
            print(f"MOVE {file_path} to Trash")
    except PermissionError as e:
        if hasattr(e, 'winerror') and e.winerror in (5, 32):
            reason = "access denied" if e.winerror == 5 else "file is in use"
            print(f"Skipped {file_path} due to {reason}")
    except Exception as e:
        if hasattr(e, 'winerror') and e.winerror == -2144927705:
            print(f"Skipped {file_path} due to OLE error -2144927705")
        else:
            print(f"Failed to delete {file_path}, Reason: {e}")

# Build the full list of file paths first
all_file_paths = []
for folder_path in folder_lists:
    try:
        entries = os.listdir(folder_path)
        for filename in entries:
            file_path = os.path.join(folder_path, filename)
            all_file_paths.append(file_path)
    except Exception as e:
        print(f"Could not list {folder_path}: {e}")
        continue

# Use threads to process deletions faster
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(try_send_to_trash, all_file_paths)

print("Done")
#input("Press Enter to close...")
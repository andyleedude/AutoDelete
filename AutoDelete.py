import os, shutil
import send2trash

user_name = os.getlogin()

folder_lists = \
    [fr"C:\Users\{user_name}\AppData\Local\Temp",
     fr"C:\Users\{user_name}\AppData\Local\NVIDIA\DXCache",
     fr"C:\Users\{user_name}\AppData\Local\D3DSCache",
     fr"C:\Users\{user_name}\AppData\Local\CrashDumps",
     r"C:\Windows\Prefetch"]
# Add the raw path of the folder that you want to clean
# Have to run as admin to delete prefetch folder
# you can run faster without using os.getlogin
for folder_path in folder_lists:
    for filenames in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filenames)
        try:
            if os.path.isfile(file_path):
                send2trash.send2trash(file_path)
                print("MOVE %s to Trash" % (file_path))
                #os.unlink(file_path)
            elif os.path.isdir(file_path):
                send2trash.send2trash(file_path)
                print("MOVE %s to Trash"%(file_path))
                #shutil.rmtree(file_path)
        except PermissionError as e:
            if e.winerror == 5 or e.winerror==32:
                print("Skipped %s " %(file_path))
                continue
        except Exception as e:
                print("Failed to delete %s, Reason: %s" %(file_path, e))

import threading as th
import multiprocessing as mp
import time
from histogram import create_histogram


def assign_histogram_creations(image_list):
    for image in image_list:
        create_histogram(image["path"]+"-original"+image["extension"], image["path"]+"-histogram"+image["extension"])
        create_histogram(image["path"]+"-edited"+image["extension"], image["path"]+"-histogram"+image["extension"])

def btn_task(self, threads: int, path, histogram: bool = True):
    thread_list = []
    list_forprocess = []
    
    for i in range(0, threads):
        list_forprocess.append([])

    list_index = 0
    for file in path:
        list_forprocess[list_index].append(file)
        list_index = list_index + 1
        if list_index == len(list_forprocess):
            list_index = 0
    
    # Delete excess threads if any
    temp_index = 0
    while temp_index < len(list_forprocess):
        if len(list_forprocess[temp_index]) == 0:
            list_forprocess.remove(list_forprocess[temp_index])
        else:
            temp_index = temp_index + 1
    
    for l in list_forprocess:
        t = th.Thread(target=btn_task_exec, args=(self, l,))
        thread_list.append(t)
        t.start()

    # Waits for all threads to finish

    while any(thread.is_alive() for thread in thread_list):
        time.sleep(0.25)
    #if histogram:
        #p = mp.Process
    print("All done")
    return thread_list

def btn_task_exec(self, files: list, histogram: bool = True, prefix: str = "temp/"):
    for file in files:
        self.imgmp(file)
        #if histogram:
        #    create_histogram(prefix+file, prefix+"histogram-"+file)
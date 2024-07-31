import threading as th
import multiprocessing as mp
import time
import asyncio

def btn_task(self, threads: int, path):
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

    print("All done")
    return thread_list

def btn_task_exec(self, files: list, prefix: str = "temp/"):
    for file in files:
        self.algorithm.assigner(self, file)
import threading as th

def btn_task(self, threads: int, path):
    thread_load = len(path) // threads
    loaded_threads = 0
    file_index = 0
    thread_list = []
    while len(path) > file_index:
        print(f"Loaded threads: {loaded_threads}")
        for i in range(0, thread_load):
            print(len(path), file_index)
            if len(path)-1 <= file_index:
                break
            t = th.Thread(target=self.imgmp, args=(path[file_index]))
            print(f"Adding thread of file {path[file_index]}")
            file_index = file_index + 1
            thread_list.append(t)
            t.start()
        loaded_threads = loaded_threads + 1
            
        if len(path) > file_index:
            print(loaded_threads, threads)
            break
    return thread_list
import time
def timemeasure(self, threads, start):
    #finished = all(not thread.is_alive() for thread in threads)
    #while not finished:
    #    finished = all(not thread.is_alive() for thread in threads)
    while threads.is_alive():
        time.sleep(0.125)
        continue
    end = time.time()
    print(f"Finished. It took {round(end-start, 2)}s.")
import tqdm


def worker(input, output):
    for idx, func, data in iter(input.get, 'STOP'):
        result = func(data)
        output.put((idx, result))


def multi_process(func, iterable, nworkers):
    from multiprocessing import Process, Queue
    NUMBER_OF_PROCESSES = nworkers
    results = []

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for idx, task in enumerate(iterable):
        task_queue.put((idx, func, task))

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # get result
    for _ in tqdm(range(len(iterable))):
        results.append(done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    results.sort(key=lambda x: x[0])
    return [x[1] for x in results]
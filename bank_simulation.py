import threading
import time
import random

NUM_TELLERS = 1
NUM_CUSTOMERS = 3

printLock = threading.Semaphore(1)
customerForTeller = [None] * NUM_TELLERS
customerAssigned = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
customerIntroduced = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]

def log_line(thread_type, thread_id, other_type=None, other_id=None, msg=""):
    printLock.acquire()
    if other_type is None:
        print(f"{thread_type} {thread_id} []: {msg}")
    else:
        print(f"{thread_type} {thread_id} [{other_type} {other_id}]: {msg}")
    printLock.release()

def teller_thread(teller_id):
    log_line("Teller", teller_id, msg="ready to serve")
    for _ in range(NUM_CUSTOMERS):
        log_line("Teller", teller_id, msg="waiting for a customer")
        customerAssigned[teller_id].acquire()
        customerIntroduced[teller_id].acquire()
        customer_id = customerForTeller[teller_id]
        log_line("Teller", teller_id, "Customer", customer_id, "serving a customer")

def customer_thread(customer_id):
    time.sleep(random.randint(0, 30) / 1000.0)
    log_line("Customer", customer_id, msg="going to bank.")
    log_line("Customer", customer_id, msg="entering bank.")
    log_line("Customer", customer_id, msg="getting in line.")
    teller_id = 0
    log_line("Customer", customer_id, msg="selecting a teller.")
    log_line("Customer", customer_id, "Teller", teller_id, "selects teller")
    customerForTeller[teller_id] = customer_id
    customerAssigned[teller_id].release()
    log_line("Customer", customer_id, "Teller", teller_id, "introduces itself")
    customerIntroduced[teller_id].release()

threads = []
threads.append(threading.Thread(target=teller_thread, args=(0,)))
threads[0].start()

customerThreads = []
for i in range(NUM_CUSTOMERS):
    customerThreads.append(threading.Thread(target=customer_thread, args=(i,)))
    customerThreads[i].start()

for i in range(NUM_CUSTOMERS):
    customerThreads[i].join()

threads[0].join()
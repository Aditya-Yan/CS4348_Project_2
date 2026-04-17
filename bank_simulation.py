import threading
import random
import time
from collections import deque

NUM_TELLERS = 3
NUM_CUSTOMERS = 10

printLock = threading.Semaphore(1)
lineLock = threading.Semaphore(1)
readyTellerCount = threading.Semaphore(0)
manager = threading.Semaphore(1)
safe = threading.Semaphore(2)
readyTellers = deque()
customerForTeller = [None] * NUM_TELLERS
transactionForTeller = [None] * NUM_TELLERS
shutdownTeller = [False] * NUM_TELLERS

customerAssigned = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
customerIntroduced = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
askTransaction = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
transactionGiven = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
transactionDone = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
customerLeft = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]


def log_line(thread_type, thread_id, other_type=None, other_id=None, msg=""):
    printLock.acquire()
    if other_type is None:
        print(f"{thread_type} {thread_id} []: {msg}")
    else:
        print(f"{thread_type} {thread_id} [{other_type} {other_id}]: {msg}")
    printLock.release()


def teller_ready(teller_id):
    lineLock.acquire()
    readyTellers.append(teller_id)
    lineLock.release()
    readyTellerCount.release()


def teller_thread(teller_id):
    log_line("Teller", teller_id, msg="ready to serve")
    while True:
        teller_ready(teller_id)
        log_line("Teller", teller_id, msg="waiting for a customer")
        customerAssigned[teller_id].acquire()
        if shutdownTeller[teller_id]:
            return
        customerIntroduced[teller_id].acquire()
        customer_id = customerForTeller[teller_id]
        transaction = transactionForTeller[teller_id]
        log_line("Teller", teller_id, "Customer", customer_id, "serving a customer")
        log_line("Teller", teller_id, "Customer", customer_id, "asks for transaction")
        askTransaction[teller_id].release()
        transactionGiven[teller_id].acquire()
        log_line("Teller", teller_id, "Customer", customer_id, f"handling {transaction} transaction")
        if transaction == "withdrawal":
            log_line("Teller", teller_id, "Customer", customer_id, "going to the manager")
            manager.acquire()
            log_line("Teller", teller_id, "Customer", customer_id, "getting manager's permission")
            time.sleep(random.randint(5, 30) / 1000.0)
            log_line("Teller", teller_id, "Customer", customer_id, "got manager's permission")
            manager.release()
        log_line("Teller", teller_id, "Customer", customer_id, "going to safe")
        safe.acquire()
        log_line("Teller", teller_id, "Customer", customer_id, "enter safe")
        time.sleep(random.randint(10, 40) / 1000.0)
        log_line("Teller", teller_id, "Customer", customer_id, "leaving safe")
        safe.release()
        log_line("Teller", teller_id, "Customer", customer_id, f"finishes {transaction} transaction.")
        transactionDone[teller_id].release()
        log_line("Teller", teller_id, "Customer", customer_id, "wait for customer to leave.")
        customerLeft[teller_id].acquire()


def customer_thread(customer_id):
    transaction = random.choice(["deposit", "withdrawal"])
    log_line("Customer", customer_id, msg=f"wants to perform a {transaction} transaction")
    time.sleep(random.randint(0, 100) / 1000.0)
    log_line("Customer", customer_id, msg="going to bank.")
    log_line("Customer", customer_id, msg="entering bank.")
    log_line("Customer", customer_id, msg="getting in line.")
    readyTellerCount.acquire()
    lineLock.acquire()
    teller_id = readyTellers.popleft()
    lineLock.release()
    log_line("Customer", customer_id, msg="selecting a teller.")
    log_line("Customer", customer_id, "Teller", teller_id, "selects teller")
    customerForTeller[teller_id] = customer_id
    transactionForTeller[teller_id] = transaction
    customerAssigned[teller_id].release()
    log_line("Customer", customer_id, "Teller", teller_id, "introduces itself")
    customerIntroduced[teller_id].release()
    askTransaction[teller_id].acquire()
    log_line("Customer", customer_id, "Teller", teller_id, f"asks for {transaction} transaction")
    transactionGiven[teller_id].release()
    transactionDone[teller_id].acquire()
    log_line("Customer", customer_id, "Teller", teller_id, "leaves teller")
    customerLeft[teller_id].release()


tellerThreads = []
customerThreads = []

for i in range(NUM_TELLERS):
    tellerThreads.append(threading.Thread(target=teller_thread, args=(i,)))
    tellerThreads[i].start()

for i in range(NUM_CUSTOMERS):
    customerThreads.append(threading.Thread(target=customer_thread, args=(i,)))
    customerThreads[i].start()

for i in range(NUM_CUSTOMERS):
    customerThreads[i].join()

for i in range(NUM_TELLERS):
    shutdownTeller[i] = True
    customerAssigned[i].release()

for i in range(NUM_TELLERS):
    tellerThreads[i].join()
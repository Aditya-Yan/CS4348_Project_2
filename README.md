# GITHUB LINK

https://github.com/Aditya-Yan/CS4348_Project_2


## Overview

This project implements a multithreaded simulation of a bank system using Python. The simulation shows the interactiosn between tellers and customers where proper synchronization is enforced using semaphores. This allows managing of shared resources and correct execution order.

The system includes 3 teller threads, 50 customer threads, shared resources(manager, safe, and bank door), and a synchronized queue

---

# Files

## bank_simulation.py
This is the main program that the user runs.

Features:
- Multithreaded: Each customer and teller runs as an independent thread
- Semaphores: Synchronization and access to shared resources using semaphores
- Resource Constraints: Only 2 tellers can access the safe at once, only 2 customers can access the door at once, and only one teller can access the manager at once
- Interaction: Customers randomly choose between deposit and withdrawal. Withdrawal goes to the manager then safe. Deposit goes directly to the safe.

# How to Run the Program

## Requirements
- Python 3 installed
- type "python bank_simulation.py" in terminal

# Notes

- This program assumes that only two customers can access the door at a time applies to leaving customers as well
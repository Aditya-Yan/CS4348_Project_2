# Development Log

## 04-16-26 11:39 PM

### Session 0

In this project I need three teller threads and fifty customer threads. What I think will be the most difficult to implement is going to be the interaction between the threads as outlined in the description of the project. To do this, I want to use semaphores to control access to shared resources, such as the safe, the manager, and the bank door. I also need to use semaphores to coordinate interactions between customers and tellers. I think to reduce complexity and ease debugging, I will first implement this project with a fewer amount of threads and then scale.

### Plan

1. Start with teller-customer interaction
2. Add teller selection and shared ready-teller structure
3. Add the transaction request and response
4. Add the manager and safe as shared resources with semaphores
5. Add bank opening logic and the two-person door restriction
6. Scale the program up to all three tellers and fifty customers and make sure everything works correctly
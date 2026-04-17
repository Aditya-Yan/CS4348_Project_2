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

## 04-16-26 11:53 PM

### Session 1

I am going to start off with a very small interaction: one teller and three customers. The goal of this session is to just make sure that a customer thread can choose a teller, introduce itself, and make sure that the threads act in a predictable way that I want them to.

### Plan

- Create one teller thread and three customer threads
- Use semaphores to synchronize customer assignment and customer introduction
- Make sure my code looks like the sample code starting now so I don't have to change things later

### Session Reflection

I managed to succesfully implement the introduction so that it looks like the sample output (on a much smaller scale). The customer thread logs that it is going to the bank, entering, getting in line, selects the teller, and introduces itself. The teller waits on semaphores and the logs that it is serving the customer. To do this I used global shared arrays and semaphore lists. This section was a little more challenging than I thought it would be. I initially had threads printing in inconsistent orders because I messed up how I was using my semaphores.

## 04-17-26 12:14 PM

### Session 2

Now that the initial interaction is working, I want to expand to a three-teller setup and add the ready-teller selection mechanism so that customers can choose from whichever teller is free.

### Plan

- Increase to three teller threads
- Add a shared queue of ready tellers
- Protect the queue with a lock
- Let customers wait until a teller is available before selecting one

### Mid-Session Thought

I am realizing how important semaphores are when using multiple threads. I initially just used a normal queue of available tellers, but without protection two customers went for the same teller. This created a race condition.

### Session Reflection

I finished making the shared scheudling structure. I made a ready-telller queue and once a teller becomes available, it puts its ID into the queue and releases a semaphore counting the number of ready tellers. Using semaphores here is key as I found out because otherwise two customers went for the same teller. Each customer waits until a teller is available, pops a teller ID, and continues as normal.


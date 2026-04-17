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

## 04-17-26 12:40 PM

### Session 3

Now that the customer and teller meet correctly and do basic interactions correctly, I added the transaction exchange. 

### Plan

- Let each customer choose deposit or withdrawal randomly
- Have tellers ask for the transaction
- Have customers respond with the transaction
- Make customers wait until the teller says the transaction is finished

### Session Reflection

I added the new semaphores so that the teller could ask for the transaction and wait on the customer to respond so the output is ordered correctly. I initially faced some challenges with this section as I was trying to just use one semaphore for the entire interactoin, but then I realized there were several synchronizatoin points. As such, I realized one was not enough. I just made a placeholder "transaction" for now as I mentioned before in the plan to simulation withdrawing or depositing. Once this is done, the customer is notified. I also scaled the project up a little bit more to 10 customer threads just to see if it would still work and it does. I believe with this I have the backbone of the project done, now I just need to implement the finer details.

## 04-17-26 01:03 PM

### Session 4

Now that I have completed the backbone of this project with the placeholder transaction interactions being done, I need to add the behind the scenes details. For this, I need to add the two major shared resources being the manager and the safe.

### Plan

- Protect the manager with a semaphore value of 1
- Protect the safe with a semaphore value of 2

### Mid-Session thought

It is really important that the placement of the acquire and releases because I was forgetting to place some here and there and it would freeze the progress since it caused multiple tellers to be blocked. It is also amazing to see how powerful of a tool semaphores are as I was just playing around with the initial semaphore values to see how it would affect the program.

### Session Reflection

Finished adding the manager and the safe and the project is now beginning to heavily resemble the final output. As seen in the log, the teller is now logging when they are going to the manager, gets their permission, or goes to the safe. The tellers are waiting properely if the manager is occupied or the safe is taken by two other tellers. As mentioned before, I had some issues with placement of the semaphores as forgetting made the whole program go haywire. 

## 04-17-26 01:17 PM

### Session 5

Adding one of the final pieces of the project, the behavior of the bank and the door restriction for customers

### Plan

- Make sure that customers can't enter bank before it is open/tellers are ready
- Make an event where bank opens so customers enter
- Add a semaphore of value 2 for the door similar to the safe
- Make customers use the door when entering and leaving (I am assuming the door limit applies when leaving too)

### Mid-Session thought

I need to create a sequence of events because right now the Customer threads are created independently of the Teller threads. I need to create a sequence that checks if all three tellers are ready, then does the bank open event. From there, everything is normal.

### Session Reflection

Finished the last two missing pieces. I used an event as I mentioned so that the customer threads block until the tellers are ready, which then does the bank open event. Then I added the door semaphore with a value two so only two customers can be using the door at once. This was not as bad as it was very similar to the safe behavior. I used it for both entering and leaving the bank as I mentioned above. Everything is working as it should, all that is left to do is to scale and make sure shut down happens well. 


## 04-17-26 01:30 PM

### Session 6

As mentioned above, just scaling and making sure that shutdown happens well.

### Plan

- Scale to 50 customer threads
- Make sure shutdown logic is good so nothing is hanging

### Session Reflection

I just increased the simulation to have 50 customers. Also checked that each teller is released after all customer threads are done, so they are not stuck forever. I also realized that I had it so that the teller currently reads the customer’s transaction before the customer officially signals that it has been given, so I should move that read to after the transaction semaphore wait, just a small fix. From what I have checked, the output format matches what is given and I have fulfilled the requirements. Also I just realized I forgot to add my main function this entire time so I just added that really quickly.
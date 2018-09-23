# Condu a Python 3.6 client for Conductor
The previous client was written in python 2.7.
This client was built upon the previous work and extended with 
added functionalities and performance boosts.


Provides 3 sets of functions:

1. Workflow management APIs (start, terminate, get workflow status etc.)
2. Worker execution framework
3. Task and Workflow definitions

## Install
This library is also in the PyPi repository and you can install it doing


    pip install condu


## Folders
* tests  - Has unit tests using the **pytest** lib
* sample - In this folder we can observe code examples of how to orchestrate, define and execute workflows
* condu  - This is the src folder with all the code

## Using Workflow Management API
Python class ```Condu``` provides client API calls to the conductor server to start manage the workflows.

## The one made by Netflix had the following problems:
              
* It was written in Python 2.7.
 This version of the Python language will stop being officially maintained at the start of 2020.
  Making it a temporary solution and not worth the investment.
  
* Netflix says their client is still in development but I did not see a code commit in over 5 months.

* It only supported workflow management (start, terminate, get workflow status etc...)
 and the execution of tasks by the workers. 
 In contrast, the definition of tasks and workflows was not supported.

* The code necessary to use it seemed a lot verbose for a Python library.

I corrected a few bugs on their library; and by addressing the problems stated above, an improved one was created.

The performance of the execution of tasks was improved by using processes instead of threads.
This change increases the performance when a worker is executing multiple tasks due to the fact that
, in Python, because of the Global Interpreter Lock (GIL), threads are not truly parallelized, only concurrent.

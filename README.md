# collection_of_mini_projects
A collection of projects that were developed by Bruno Lopes
note: read the 'README.md' inside each project

##	 video_silence_remover
A tool that removes the portions of a mp4 video that are deemed silent.
It has a React interface, a back-end REST api developed in python/flask, and a Mongo database.

## Condu
This is a python library used to interface with the orchestration engine **Netflix Conductor**

The one made by Netflix had the following problems:
              
* It was written in Python 2.7.
 This version of the Python language will stop being officially maintained at the start of 2020.
  Making it a temporary solution and not worth the investment.
  
* Netflix says their client is still in development but I did not see a code commit in over 5 months.

* It only supported workflow management (start, terminate, get workflow status etc...)
 and the execution of tasks by the workers. 
 In contrast, the definition of tasks and workflows was not supported.

* The code necessary to use it seemed a lot verbose for a Python library.

I corrected a few bugs on their library, and by addressing the problems stated above, an improved one was created.

The performance of the execution of tasks was improved by using processes instead of threads.
This change increases the performance when a worker is executing multiple tasks due to the fact that,
 in Python, because of the Global Interpreter Lock (GIL), threads are not truly parallelized, only concurrent.


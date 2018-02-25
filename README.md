# HackCU-2018
Alteryx Challenge

We worked in team of 2: Myself(Vibhor Mishra) and Prasanna Kumar Srinivasachar

We mostly relied on Python for data processing and hitting URL to fetch data. Figuring out what binary data represents was the tricky part and even after we figured that out, it was hard to figure out what actually is being asked in the challenge question. We assumed that we have to call the URLs, fetch JSON and sum up the elements decoded with the URLs to output the attendence of the event. We didn't get any other attendence related info anywhere else with it. And the sum that we got from summing up count related URLs also came up close to the HackCU event headcount.

Here is the code flow:

1) Alteryx data file **HackCU2018_AlteryxChallenge.yxdb** is read in read data step of workflow where the binary data is read.
2) It then calls the **run command**  step which calls Python executable that we have created, with **Write Source** as the csv file written by Alteryx that has binary data, path of pthon executable in **Command** and results.csv in **Read Input** to read the output of python file into Alteryx.
3) The following tasks are performed in python file (which is converted to exe and used in Alteryx as there was some error in executing .py file directly in there):
   * Convert Binary data to ascii chars by reading 8 bits at a time and converting them to corresponding ascii values
   * It results in the following URLs:
      * https://data.cityofnewyork.us/api/views/kku6-nxdu,columns.0.cachedContents.top.16.count,0
      *	https://data.kingcounty.gov/api/views/b27z-cdmk,columns.3.cachedContents.null,2      
      * ........
      * ........
   * We then hit those URLs and fetch the JSON response and extract the elememnt's value mentioned with each URL like mentioned in this: (,columns.3.cachedContents.null,2).
   * Only those URLs are hit which have "count" field mentioned with them and thus, counting only those results because the chanllenge says, to count the attendance at this event. So, we thought that URLs with count mentioned with them(to fetch from JSON) only would make sense here.
   * Finally we total the count and store in Results.csv which is read in Alteryx.
   
   
I hope what we calculated makes sense and is the output expected from us.

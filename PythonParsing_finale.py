
# coding: utf-8

# In[73]:


import json
import csv, sys
import urllib.request

maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


#Read data from csv written by Alteryx
file = open('binaryValues.csv', 'r')
reader = csv.reader(file)
data = []
for row in reader:
    data.append(row)

file.close()


# In[74]:


from collections import defaultdict

#Convert Binary data to ascii chars
def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))


# In[75]:


decoded = decode_binary_string(data[1][0])

# Results from above statement
#	https://data.cityofnewyork.us/api/views/kku6-nxdu
#	https://data.kingcounty.gov/api/views/b27z-cdmk
#	https://data.montgomerycountymd.gov/api/views/icn6-v9z3
#	https://data.iowa.gov/api/views/s3p7-wy6w
#	https://data.maryland.gov/api/views/f53i-bwcd
#	https://data.baltimorecity.gov/api/views/xviu-ezkt
#.......
#.......

# In[76]:


#Function to form JSON element selector to fetch the values from corresponding selectors mention with the URL
def getAssocVal(arr,jsonData):
    idx = 0
    val = jsonData.get(arr[idx])
    l = len(arr)
    while l > idx + 1:
        if arr[idx + 1].isnumeric():
            if len(val) >= int(arr[idx + 1]):
                val = val[int(arr[idx + 1])].get(arr[idx + 2])
            else:
                val = 0
            idx += 2
        else:
            val = val.get(arr[idx + 1])
            idx += 1
    return val


# In[77]:


urlsToArr = defaultdict(list) 
urlsToJson = dict()


# In[78]:


for s in decoded.split("https\x9e//")[1:]:
    url = s.split(",")[0]
    tempArr = s.split(",")[1]
    if urlsToArr.get(url,None) is None:
        urlsToArr[url] = []
    urlsToArr.get(url).append(tempArr)


# In[79]:


#urlsToArr.keys()


# In[80]:


for url in urlsToArr.keys():
    tUrl = 'https://' + url
    urlsToJson[tUrl] = urllib.request.urlopen(tUrl).read()


# In[81]:


# Hitting only those URLs which have "count" filed mentioned with them and thus, counting only those results 
# because the chanllenge says, to count the attendance at this event. So, we thought that URLs with count mentioned 
# with them(to fetch from JSON) only would make sense here.
cn = 0.0
for k in urlsToJson.keys():
    for s in urlsToArr.keys():
        if k[8:] == s:
            for arr in urlsToArr.get(s):
                if arr.find('.') > 0 and 'count' in arr:
#                     print k , arr
                    t = getAssocVal(arr.split('.'),json.loads(urlsToJson.get(k)))
#                     print(t)          
                    cn += t

# In[83]:

#Writing total count  to the file
f = open("results.csv","w")
f.write("Results\n")
f.write(str(cn))
f.close()


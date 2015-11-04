import mincemeat
import glob
import time

t0 = time.time()

all_files = glob.glob("GutenbergSF/*.*")
def file_contents(file_name):
    f = open(file_name, encoding="Latin-1")
    try:
        return f.read()
    finally:
        f.close()
datasource = dict((file_name, file_contents(file_name)) for file_name in all_files)


def mapfn(k, v):
    from stopwords import allStopWords
    for w in v.split():
	    w = re.sub(r'[^\w\s]','',w)
		w = w.lower()
        if w in allStopWords or len(w)==1:
            yield w, 0
        else:
            yield w, 1

def reducefn(k, vs):
    result = 0
    for v in vs:
        result += v
    return result

s = mincemeat.Server()

s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
#sort results from high to low
results = sorted(results.items(), key=lambda x: x[-1], reverse=True)
#print results
i = open('outfile.txt','w')
i.write(str(results))
i.close()

t1 = time.time()
total = t1-t0
j = open('time.txt', 'w') 
j.write(str(total))
print(results)
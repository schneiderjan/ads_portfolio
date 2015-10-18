import mincemeat
import glob


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
	     if w not in allStopWords:
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


print(results)
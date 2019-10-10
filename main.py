import pandas as pd
import os
from pprint import pprint
import csv

'''
get search results whos sources have the highest citescore
'''

ignore = {'2-s2.0-85023612767', '2-s2.0-85055178570', '2-s2.0-84927624380', '2-s2.0-85043353825', '2-s2.0-84896338572', '2-s2.0-84908338932', '2-s2.0-84984662709', '2-s2.0-85016248484', '2-s2.0-84896338572', '2-s2.0-85004073474', '2-s2.0-85047371349', '2-s2.0-85048895166', '2-s2.0-85064652461', '2-s2.0-84904464337', '2-s2.0-84980408188', '2-s2.0-85010889946', '2-s2.0-84890804101'}

ignorecb = {'2-s2.0-85057886918', '2-s2.0-85041543184', '2-s2.0-85055150567', '2-s2.0-85061200967', '2-s2.0-85066015524', '2-s2.0-85067369527', '2-s2.0-85067463974', '2-s2.0-85067624629', '2-s2.0-85068211053', '2-s2.0-85068315655', '2-s2.0-85068539775', '2-s2.0-85057279298', '2-s2.0-85059651190', '2-s2.0-85063688194', '2-s2.0-85064541185', '2-s2.0-85066501477', '2-s2.0-85069815265', '2-s2.0-85070561914', '2-s2.0-85070740250', '2-s2.0-85071332918', '2-s2.0-85072032697', '2-s2.0-85058436465', '2-s2.0-85064979369', '2-s2.0-85067656645', '2-s2.0-85068858618', '2-s2.0-85072387960'}
thld_ref = 3
thld_cb = 4
citescore = 1.0
yearContraint = True
fromyear = 2014
toyear = 2019
 
def papersNotInDatabase(paper_ids, folder='./database'):
	print("# papers to save:", len(paper_ids))
	
	# compare to paper ids already saved
	file_ids = set([file.split('.csv')[0] for file in os.listdir(folder)])
	print("# papers already saved:", len(file_ids))
	
	papers_left = paper_ids.difference(file_ids)
	print("# papers left to save:", len(papers_left))
	
	return papers_left

def getSeedPapers():
	# read search file
	seeds = ['./source/digitaltrans_2014-2019_keywords_200rel(2).csv', './source/digitaltrans_2014-2019_keywords_201-400rel(2).csv', './source/digitaltrans_2014-2019_keywords_401-600rel(2).csv']
	
	li = []
	for filename in seeds:
		df = pd.read_csv(filename, index_col=None, header=0, usecols = ["Source title"])
		li.append(df)

	df = pd.concat(li, axis=0, ignore_index=True)

	#df = pd.read_csv(seed, usecols = ["Source title"])
	search_titles = df.values.tolist()
	search_titles = list(set([x[0] for x in search_titles]))
	search_titles = sorted(search_titles)
	
	paper_source_score = getTopSourceTitles(search_titles)
	
	# use papers with top source score
	li = []
	for filename in seeds:
		df = pd.read_csv(filename, index_col=None, header=0)
		li.append(df)

	df = pd.concat(li, axis=0, ignore_index=True)
	
	df = df.loc[df['Source title'].isin(paper_source_score)]
	
	paper_ids = set([row.EID for index, row in df.iterrows()])
	
	db = dict()
	for id in paper_ids:
		db = initPaper(db, id)
	
	return db, paper_source_score

def getTopSourceTitles(search_titles):
	# read source citescore file
	csv_file = './data/CiteScore_Metrics_2011-2018_download.csv'
	df = pd.read_csv(csv_file, usecols = ["Title", "CiteScore"])
	source_names = df.values.tolist()
	source_names = {x[0]: x[1] for x in source_names}

	print("# source titles:", len(source_names))
	
	# separate paper sources that have citescores and those that do not
	paper_source_score = []
	paper_source_other = []
	for st in search_titles:
		if st in source_names:
			paper_source_score.append([source_names[st], st])
		else:
			pass
			
	paper_source_score = sorted(paper_source_score, reverse=True)
	
	print("# seed source titles:", len(search_titles))
	print("# seed source titles with scores:", len(paper_source_score))
	#pprint(paper_source_score)
	
	# reduce sources with the highest scores
	paper_source_score = set([x[1] for x in paper_source_score if x[0]>=citescore])
	#pprint(paper_source_score)
	print("# seed source titles with top scores:", len(paper_source_score))
	
	return paper_source_score
	
def printReport(db, db_ref, db_cb, cnt):
	
	db_true_ref = [[key, val] for key, val in db.items() if (len(val["ref_src"])) >= thld_ref]
	
	db_true_cb = [[key, val] for key, val in db.items() if (len(val["cb_src"])) >= thld_cb]
	
	print("Round %s" % (cnt))
	print("# papers in db:", len(db))
	print("# papers in db found through refs:", len(db_true_ref))
	print("# papers in db found through cite bys:", len(db_true_cb))
	print("# papers referened to add to db:", len(db_ref))
	print("# papers cite by to add to db:", len(db_cb))
	print()
	
def printReportToCSV(db):
	headers = ["# cited by in db", "# ref in db", "Authors", "Author(s) ID", "Title", "Year", "Source title", "Volume", "Issue", "Art. No.", "Page start", "Page end", "Page count", "Cited by", "DOI", "Link", "ids that cite paper", "ids that paper refs"]
	report_list = [[len(val['ref_src'])] + [len(val['cb_src'])] + val['info'][:14] + [val['ref_src']] + [val['cb_src']] for key, val in db.items()]
	
	report_list.sort(key=lambda x: x[1], reverse=True)
	report_list.sort(key=lambda x: x[0], reverse=True)
	
	report_list = [headers] + report_list
	
	with open('./database/db.csv', 'w', newline='') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		for ls in report_list:
			wr.writerow(ls)
	
def getPapersInDatabase():
	
	db, paper_source_score = getSeedPapers()
	print("# final seed papers (with top source scores):", len(db))
	
	len_db_prev = 0
	db_ref = set()
	db_cb = set()
	cnt = 0
	while(True):
		cnt += 1
		db, ref = getPapersMostReferenced(db)
				
		db, cb = getPapersMostCitedby(db, paper_source_score)
		
		db_ref = db_ref.union(ref)
		db_cb = db_cb.union(cb)
		
		printReport(db, db_ref, db_cb, cnt)
		
		#if len(db) == 155:
		#	break
		
		if len(db) == len_db_prev:
			break
			
		len_db_prev = len(db)
		
	#pprint(db_ref)
	#pprint(db_cb)
	
	printReportToCSV(db)
	
def initPaper(db, id):
	db[id] = dict()
	db[id]["info"] = []
	db[id]["cb_src"] = set()
	db[id]["ref_src"] = set()
	return db
	
def dbRules(val):
	return len(val["ref_src"]) >= thld_ref or len(val["cb_src"]) >= thld_cb
	
def dbReduce(db):
	return {id: val for id, val in db.items() if dbRules(val)}	
	
def getPapersMostCitedby(db, paper_source_score, folder='./database/citeby'):
	
	# papers we are interested in comparing references
	paper_ids = set(db.keys())
	paper_ids = paper_ids.difference(ignore)
	paper_ids = paper_ids.difference(ignorecb)
	
	# get list of files already fetched reference folder
	file_ids = set([file.split('.csv')[0] for file in os.listdir(folder)])
	
	keep = set()
	for pid in paper_ids:
	
		# check if paper is in list of files already fetched
		if pid in file_ids:
			file = ''.join([pid, '.csv'])
			file = os.path.join(folder, file)
			
			df = pd.read_csv(file)
			
			# include extra source verifier
			df = df.loc[df['Source title'].isin(paper_source_score)]
			
			if yearContraint:
				df = df[df.Year>=fromyear]
				df = df[df.Year<=toyear]
			
			for index, row in df.iterrows():
				eid = row.EID
				row = row.values.tolist()
				
				if eid not in db:
					db = initPaper(db, eid)

				db[eid]["info"] = row
				db[eid]["cb_src"] = db[eid]["cb_src"].union({pid})
				
		else:
			keep.add(pid)
				
	db = dbReduce(db)
	
	return db, keep

def getPapersMostReferenced(db, folder='./database/reference'):
	# papers we are interested in comparing references
	paper_ids = set(db.keys())
	paper_ids = paper_ids.difference(ignore)
	
	# get list of files already fetched reference folder
	file_ids = set([file.split('.csv')[0] for file in os.listdir(folder)])
	
	keep = set()
	for pid in paper_ids:
		# check if paper is in list of files already fetched
		if pid in file_ids:
			file = ''.join([pid, '.csv'])
			file = os.path.join(folder, file)
			
			df = pd.read_csv(file)
			
			if yearContraint:
				df = df[df.Year>=fromyear]
				df = df[df.Year<=toyear]
			
			for index, row in df.iterrows():
				eid = row.EID
				row = row.values.tolist()
				if eid not in db:
					db = initPaper(db, eid)
				db[eid]["ref_src"] = db[eid]["ref_src"].union({pid})
				db[eid]["info"] = row
		else:
			keep.add(pid)
				
	db = dbReduce(db)	
	
	return db, keep
	
if __name__ == '__main__':
	
	getPapersInDatabase()
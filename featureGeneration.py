# -*- coding: utf-8 -*-
from __future__ import division
import math
import os
import pickle

os.chdir("E:\\5. Innovation")

blocks = pickle.load( open( "blocks.p", "rb" ) )
blocks_with_features = []
features_progress = open("features.txt", "wb")
features_progress.write("Name, Paper1 ID, Paper2 ID, Features[To be detailed], Label(Same Author or Different)\n")

total_papers = 320032
for key in blocks.keys():
    papers_of_this_name = len(blocks[key])
    auth_lname_idf_global = math.log( total_papers / papers_of_this_name )
    if len(blocks[key]) < 3 and len(blocks[key]) > 100:
        continue
    for i in range(len(blocks[key])):
        for j in range(i+1, len(blocks[key])):
            paper1 = blocks[key][i]
            paper2 = blocks[key][j]
  
            # Generating Feature                                                                         
            
            # IMPORTANT: YOU SHOULD ALways determine the author that matches the block then conduct
                # Author and Coauthor Similarity features!
            # Get firstname, fist initial and last of signature author of the block
            # Adjust list of coauthors if needed
            
            if paper1['signature'] == key:
                if  paper1['fname'] == None:
                    fname_A = ""
                elif paper1['fname'][1] == '.':
                    fname_A = paper1['fname'][0]
                else:
                    fname_A = paper1['fname']
                init_A = paper1['init']
                coauthors_A = []
                for coauthor in paper1['coauth']:
                    coauthors_A.append(coauthor.split(',')[0]) 
            else:
                coauthors_A = []
                coauthors_A.append(paper1['signature'].split(',')[0])
                for coauthor in paper1['coauth']:
                    if coauthor == key:
                        init_A = fname_A = coauthor[-1:]
                    else:
                        coauthors_A.append(coauthor.split(',')[0])
            
            if paper2['signature'] == key:
                if  paper2['fname'] == None:
                    fname_B = ""
                elif paper2['fname'][1] == '.':
                    fname_B = paper2['fname'][0]
                else:
                    fname_B = paper2['fname']
                init_B = paper2['init']
                coauthors_B = []
                for coauthor in paper2['coauth']:
                    coauthors_B.append(coauthor.split(',')[0])
            else:
                coauthors_B = []
                coauthors_B.append(paper2['signature'].split(',')[0])
                for coauthor in paper2['coauth']:
                    if coauthor == key:
                        init_B = fname_B = coauthor[-1:]
                    else:
                        coauthors_B.append(coauthor.split(',')[0])
            
                
            # Feature 1
            if fname_A != fname_B and len(fname_A) > 1 and len(fname_B) > 1:
                auth_fst = 0
            elif init_A != init_B and (len(fname_A) <= 1 or len(fname_B) <= 1):
                auth_fst = 1
            elif init_A == init_B and (len(fname_A) <= 1 or len(fname_B) <= 1):
                auth_fst = 2
            else:         # paper1['fname'] == paper2['fname'] and len(paper1['fname']) > 1 and len(paper2['fname']) > 1
                auth_fst = 3
            
            #auth_mid = 0
            #auth_suf = 0
            
            # Feature 2
            # check if block[key] = both papers [signature]s   <-- which means both are first authors
            if paper1['signature'] == key and paper2['signature'] == key:
                auth_ord = 2
            elif len(paper1['coauth']) > 0 and len(paper2['coauth']) > 0:
                if paper1['coauth'][-1] == key and paper2['coauth'][-1] == key:
                    auth_ord = 1
                else:
                    auth_ord = 0
            else:
                auth_ord = 0
            
            # Feature 3:
            auth_lname_idf = auth_lname_idf_global
            
            # Feature 4:
            aff_A = paper1['aff'].split() if paper1['aff'] != None else []
            aff_B = paper2['aff'].split() if paper2['aff'] != None else []
            aff_intersection = []
            for word in aff_A:
                if word in aff_B: aff_intersection.append(word)
            aff_jac = len(aff_intersection) /len(aff_A+aff_B) if len(aff_A+aff_B) != 0 else 0
            
            # Feature 5:
            coauthor_lname_shared = 0
            for coauthor in coauthors_A:
                if coauthor in coauthors_B:
                    coauthor_lname_shared += 1
            
            # Feature 6:
            keyword_shared = 0
            if paper1['keywords'] != None and paper2['keywords'] != None:
                for word in paper1['keywords']:
                    if word in paper2['keywords']:
                        keyword_shared += 1
            
            # Feature 7:
            jour_year_diff = abs( int(paper1['year']) - int(paper2['year']) )
            
            # Feature 8:
            title_A = paper1['title'].split() if paper1['title'] != None else []
            title_B = paper2['title'].split() if paper2['title'] != None else []
            title_intersection = []
            for word in title_A:
                if word in title_B: title_intersection.append(word)
            title_shared = len(title_intersection) /len(title_A+title_B) if len(title_A+title_B) != 0 else 0
            
            features = [auth_fst, auth_ord, auth_lname_idf, aff_jac, coauthor_lname_shared, keyword_shared, jour_year_diff, title_shared]
            label = 1 if paper1['aff'] == paper2['aff'] else 0                      # dummy label for now, 1 = 'Same' author if affiliation is the same and 0 ='Different' otherwise
            line = [key,paper1['UID'],paper2['UID'],features,label]
            blocks_with_features.append(line)
            features_progress.write(str(line)+"\n")
          
features_progress.close()
pickle.dump( blocks_with_features, open( "blocks_with_features.p", "wb" ) )

# To be implemented Later 
'''
aff_tfidf = 0
for word in aff_intersection:
    aff_tfidf += TFIDF(word,aff_A) * TFIDF(word,aff_A)

aff_softtfidf = 0


coauthor_lname_idf = 0
coauthor_lname_jac = 0


keyword_shared_idf = 0
keyword_tree_shared = 0
keyword_tree_shared_idf = 0

jour_shared_idf = 0
jour_lang = 0
jour_lang_idf = 0
jour_year = 0           # speical to Medline, redefine or discard for WOS?


paper1 = {'UID': u':000322415800002',
 'aff': u'Miami Univ',
 'coauth': ['Charles, H', 'Dinh, T', 'Killian, K'],
 'fname': u'Angelica V.',
 'init': u'A',
 'jour': u'JOURNAL OF INSECT PHYSIOLOGY',
 'keywords': [u'Immune',
  u'Cricket',
  u'Phenoloxidase',
  u'Lysozyme',
  u'Hemocyte',
  u'Encapsulation'],
 'lang': u'English',
 'lname': u'Pinera',
 'signature': 'Pinera, A',
 'title': u'Maturation of the immune system of the male house cricket, Acheta domesticus',
 'year': u'2013'}




paper2 = {'lang': u'English', 'jour': u'INTERNATIONAL JOURNAL OF MENTAL HEALTH NURSING', 'UID': u':000324999600009',
'title': u'Validation of the routine assessment of patient progress (RAPP) in patients with psychosis in South India',
'aff': u'Christian Med Coll & Hosp', 'signature': 'Charles, H', 'lname': u'Charles', 'init': u'H', 'fname': u'Helen Sujatha',
'year': u'2013', 'keywords': None, 'coauth': []}
'''
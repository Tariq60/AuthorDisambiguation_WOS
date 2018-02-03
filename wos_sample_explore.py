# -*- coding: utf-8 -*-
import json
import os
import pickle

os.chdir("C:\Users\Tariq\Documents\WOS")

papers = []

for f in os.listdir('.'):
    file = open(f, "r")
    #file = open("part_9.xml.orig.json","r")
    for line in file.readlines():
        try:
            jsn = json.loads(line)
            paper = {}
            paper['UID'] = jsn['UID'][3:]
            jsn = jsn['static_data']
        
            tempList = jsn['summary']['names']['name']
            coauthors = []
            if type(tempList)==list:                                     # for papers with more than one author
                paper['lname']= tempList[0]['last_name'] if 'last_name' in tempList[0] else None
                paper['fname']= tempList[0]['first_name'] if 'first_name' in tempList[0] else None
                initials = tempList[0]['wos_standard'].split()[1] if 'wos_standard' in tempList[0] and len(tempList[0]['wos_standard'].split()) > 1 else None
                for i in range(1,len(tempList)):
                    coauthor_last = tempList[i]['last_name'] if 'last_name' in tempList[i] else None
                    coauthor_finit = tempList[i]['first_name'][0] if 'first_name' in tempList[i] else None
                    coauthors.append(str(coauthor_last)+", "+str(coauthor_finit))
            else:                                                           # for papers with ONLY one author
                paper['lname']= tempList['last_name']  if 'last_name' in tempList else None               
                paper['fname']= tempList['first_name'] if 'first_name' in tempList else None
                initials = tempList['wos_standard'].split()[1] if 'wos_standard' in tempList and len(tempList['wos_standard'].split()) > 1 else None
            
        
            paper['init'] = initials[0] if initials != None else None
            #paper['mid'] = initials[1] if len(initials>1) and type(initials) == unicode else None
            paper['signature'] = str(paper['lname']) +", "+ str(paper['init'])
            paper['coauth'] = coauthors
        
            tempList = jsn['fullrecord_metadata']['addresses']['address_name'] if 'address_name' in jsn['fullrecord_metadata']['addresses'] else None
            if type(tempList)==list:
                paper['aff']= tempList[0]['address_spec']['organizations']['organization']     # for papers with multiple institutions
            elif tempList != None:
                paper['aff']= tempList['address_spec']['organizations']['organization']        # for papers with one institution
            else:
                paper['aff'] = None
            
            tempList = jsn['summary']['titles']['title']
            if type(tempList) == list:
                for item in tempList:
                    if item['type'] == 'item':
                        paper['title']= item['value']
                    elif item['type'] == 'source':
                        paper['jour']= item['value']
            
            tempList = jsn['fullrecord_metadata']['languages']['language']
            if type(tempList) == list:
                for item in tempList:
                    if item['type'] == 'primary':
                        paper['lang'] = item['value']                                           # for papers with multiple languages
            else:
                paper['lang'] = tempList['value']
            
            paper['year']= jsn['summary']['pub_info']['pubyear']    
            paper['keywords']= jsn['fullrecord_metadata']['keywords']['keyword'] if 'keywords' in jsn['fullrecord_metadata'] else None
            
            papers.append(paper)
        except:
            pass

pickle.dump( papers, open( "papers.p", "wb" ) )


'''
Blocking Function:  Papers from authors with the same signature (lastname, first initial) will be combined in one document
paperA = (lnameA, fnameA, initA, midA, sufA, coauthA, affA, titleA, jourA, langA, yearA, meshA)     << identified by UID
paperB = (lnameB, fnameB, initB, midB, sufB, coauthB, affB, titleB, jourB, langB, yearB, meshB)     << identified by UID, signatures->[lname,init] for all authors 

lnamei = the author’s last name in paperi                           summary->names->name[0,last_name]
fnamei = the author’s first name in paperi                          summary->names->name[0,first_name]
initi = the author’s first initial in paperi                        summary->names->name[0,wos_standard][first  character after ',' ]
midi = the author’s middle name in paperi, if given                 summary->names->name[0,wos_standard][Second character after ',' ] (if exists)
sufi = the author’s suffix in paperi, if given, e.g. “Jr”, “Sr”     ignore
coauthi = set of coauthors’ last name in paperi                     list_size = summary->names->count, list = summary->names->name->last_name  all but first author
affi = affiliation of the paperi’s 1st author                       fullrecord_metadata->addresses->address_name[0] if list->address_spec->organizations->organization
titlei = paperi’s title                                             summary->titles->title->[value if type = "item"]
jouri = paperi’s journal name                                       summary->titles->title->[value if type = "source"]
langi = paperi’s journal language e.g. English, Chinese             fullrecord_metadata->languages->language->[value if type = "primary"]
yeari = paperi’s year of publication                                summary->pub_info->pubyear
meshi = set of mesh terms in the paperi                             fullrecord_metadata->keywords->keyword
'''
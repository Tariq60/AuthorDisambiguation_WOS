import os
import numpy as np
import pandas as pd
os.chdir("e:\\5. Innovation")

featuresfile = open("features.txt", "rb")
size = 1000000
sample100 = np.random.choice(size,100, replace=False)
sample200 = np.random.choice(size,200, replace=False)
sample300 = np.random.choice(size,300, replace=False)
sample400 = np.random.choice(size,400, replace=False)
sample500 = np.random.choice(size,500, replace=False)

set100 = pd.DataFrame(columns=('f1','f2','f3','f4','f5','f6','f7','f8','label'))
set200 = pd.DataFrame(columns=('f1','f2','f3','f4','f5','f6','f7','f8','label'))
set300 = pd.DataFrame(columns=('f1','f2','f3','f4','f5','f6','f7','f8','label'))
set400 = pd.DataFrame(columns=('f1','f2','f3','f4','f5','f6','f7','f8','label'))
set500 = pd.DataFrame(columns=('f1','f2','f3','f4','f5','f6','f7','f8','label'))

line = featuresfile.readline()
for i in range(size):
    line = featuresfile.readline()
    line = line.split("[")[2]
    parsed_line = line.split("]")[0].split(",")
    for j in range(len(parsed_line)):
        if parsed_line[j][0] == " ":
            parsed_line[j] = float(parsed_line[j][1:])
        else:
            parsed_line[j] = float(parsed_line[j])
    parsed_line.append(line.split("]")[1].split()[1])
    
    if i in sample100:
        set100.loc[len(set100)] = parsed_line
    if i in sample200:
        set200.loc[len(set200)] = parsed_line
    if i in sample300:
        set300.loc[len(set300)] = parsed_line
    if i in sample400:
        set400.loc[len(set400)] = parsed_line
    if i in sample500:
        set500.loc[len(set500)] = parsed_line


set100.to_csv("set100.csv")
set200.to_csv("set200.csv")
set300.to_csv("set300.csv")
set400.to_csv("set400.csv")
set500.to_csv("set500.csv")

'''
from sklearn import tree
Y = (datateam[:,-1]).astype(float)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
importances = clf.feature_importances_
std = np.std(clf.feature_importances_,axis=0)
indices = np.argsort(importances)[::-1]

#------------------------

from sklearn.cross_validation import cross_val_score, ShuffleSplit
from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor
 
#Load boston housing dataset as an example
boston = load_boston()
X=np.array(X)
names = features[:,0]
 
rf = RandomForestRegressor(n_estimators=20, max_depth=4)
scores = []
for i in range(shape(X)[1]):
    score = cross_val_score(rf, X[:, i:i+1], Y, scoring="r2",
                              cv=ShuffleSplit(len(X), 3, .3))
    scores.append((round(np.mean(score), 3), names[i]))
'''



featuresfile = open("features_sample.txt", "rb")
lines = featuresfile.readlines()
sampleSet = pd.DataFrame(columns=('name','p1','p2','f1','f2','f3','f4','f5','f6','f7','f8','label'))

for i in range(len(lines)):
    line = lines[i].split("{")
    name = line[0][2:-3]
    paper1 = line[1][:-3]
    paper2 = line[2].split("}")[0]
    parsed_line = line[2].split("}")[1][3:]
    label = parsed_line.split("]")[1].split()[1]
    parsed_line = parsed_line.split("]")[0].split(",")
    for j in range(len(parsed_line)):
        if parsed_line[j][0] == " ":
            parsed_line[j] = float(parsed_line[j][1:])
        else:
            parsed_line[j] = float(parsed_line[j])
    sampleSet.loc[len(sampleSet)] = [name, paper1, paper2, parsed_line[0], parsed_line[1], parsed_line[2], parsed_line[3],
                                    parsed_line[4], parsed_line[5], parsed_line[6], parsed_line[7], label]

sampleSet.to_csv("sampleSet.csv")






from sklearn.cross_validation import cross_val_score, ShuffleSplit
from sklearn.ensemble import RandomForestRegressor


train = sampleSet['label']    #.values
target = sampleSet.loc[:, 'f1':'f8']
rf = RandomForestRegressor(n_estimators=20, max_depth=4)
rf.fit(train, target)








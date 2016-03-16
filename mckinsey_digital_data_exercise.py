"""
Ask: Given a data set of transaction (+100K rows) from a large retailer, find groups of items that are frequently purchased together. Each row
is a single transaction with a '1' denoting that item was in that transaction. 


Nirav Chitkara
"""

#import relevant libraries
import pandas as pd
import itertools, collections
from itertools import compress, combinations
from collections import defaultdict


#Extract data from csv file

COLS_NAMES = ['item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'item_6', 'item_7', 'item_8', 'item_9', 
'item_10', 'item_11', 'item_12', 'item_13', 'item_14', 'item_15', 'item_16', 'item_17', 'item_18', 'item_19',
'item_20', 'item_21', 'item_22', 'item_23', 'item_24', 'item_25', 'item_26', 'item_27', 'item_28', 'item_29',
'item_30', 'item_31', 'item_32', 'item_33', 'item_34', 'item_35', 'item_36', 'item_37', 'item_38', 'item_39',
'item_40', 'item_41', 'item_42', 'item_43', 'item_44', 'item_45', 'item_46', 'item_47', 'item_48', 'item_49']

transaction = pd.read_csv('data.csv', sep = ',', header = 0, index_col = 0, dtype = None) #read the csv file into a Pandas Data Frame

#Implement the Apriori algorithm to get frequency of items
def apriori(transaction):
	purchased = [] #list that will hold our transactions of items that were purchased 
	for idx, row in transaction.iterrows():
		purchased.append(set(compress(COLS_NAMES, row))) #remove unpurchased items and create set with names of items purchased
		
	group_1 = defaultdict(int) #first dictionary holding the count of how many of each item was purchased

	#find the counts for each singular item purchased
	for row in purchased:
		for item in row:
			group_1[item] += 1 
	print "singular item counts from all transactions:", group_1 
	print

	#filtering singular items
	for it in group_1.items(): #items returns a tuple (key, value)
		if it[1] <= 20000: #minimum support rule of removing anything less than or equal to 20% of all transactions
			del group_1[it[0]] #remove key from dictionary

	print "item counts above minimum support:", group_1 #new dictionary of filtered items
	print

	combos_1 = list(combinations(group_1.keys(), 2)) #create combination pairs from singular items above minimum support
	print "item pairs:", combos_1
	print

	group_2 = defaultdict(int) #second dictionary holding the count of how many of each item pair was purchased

	#find the frequency for item pairs in all of the transactions
	for item in combos_1: #take a pair 
		for s in purchased: #take the list of items purchased in each transaction
			if set(item).issubset(s): #if the combination pair is a subset of the transaction set
				group_2[item] += 1

	print "item pair counts:", group_2
	print

	#filtering paired items for those that aren't above minimum support 
	removed_1 = [] #list for containing removed pairs
	for item in group_2.items(): 
		if item[1] <= 20000: #filter the pairs that are below the minimum support of 20%
			removed_1.append(set(item[0]))
			del group_2[item[0]]

	print "item pair counts above minimum support:", group_2 #new dictionary of filtered item pairs
	print
	print "removed pairs:", removed_1
	print

	combos_2 = list(combinations(group_1.keys(), 3)) #create triplets from singular items above minimum support

	print "item triplets:", combos_2
	print 

	group_3 = defaultdict(int) #third dictionary holding count of how many of each item triplet was purchased 
	removed_2 = [] #empty list for containing removed triplets

	#filter list of triplets that contain as a subset any of the item pairs that were not above minimum support
	for rmved in removed_1:
		for item in combos_2:
			if rmved.issubset(set(item)):
				removed_2.append(item) #add removed triplets to list
				del item

	print "item triplets removing infrequent pair sets:", combos_2
	print
	print "removed triplets:", removed_2
	print

	#find the frequency count for all remaining triplets in all transactions
	for item in combos_2:
		for s in purchased:
			if set(item).issubset(s):
				group_3[item] +=1
	print "item triplet counts:", group_3
	print

	removed_3 = [] #empty list for containing removed triplets that don't meet the minimum support level

	#filter remaining triplets for those that aren't above minimum support 
	for item in group_3.items():
		if item[1] <= 20000:
			removed_3.append(set(item[0]))
			del group_3[item[0]]

	print "item triplet counts above min support:", group_3
	print

apriori(transaction)


"""
After running through the Apriori alogirthm implementation, the groups of items that were most frequent above the minimum support of 20% of all
transactions are ('item_29', 'item_7', 'item_2') with a count of 21,767 and ('item_22', 'item_5', 'item_3') with a count of 21,670.
"""


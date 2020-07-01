import pandas as pd
import numpy as np
import math
import csv
from itertools import combinations

MIN_SUPPORT = int(input("Enter minimum support"))
import time
import sys
start = time.process_time()   
class recursionlimit:
    def __init__(self, limit):
        self.limit = limit
        self.old_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

with recursionlimit(15000):
        
    cd = {}
    fps = {}

    def get_ordered_itemset(file_name):
        transactions = []
        with open(file_name,'rt')as f:
            data = csv.reader(f)
            for row in data:
                transactions.append(row)
                for i in row:
                    if (type(i)!=str and math.isnan(i)) or i=='':
                        continue
                    else:
                        try:
                            cd[i] += 1
                        except:
                            cd[i] = 1
        
        ois = []
        
        for item in sorted(cd.items(),key=lambda kv:(kv[1]),reverse=True):
            fps[item[0]] = item[1]
        

        for txn in transactions:
            temp = []
            items = list(fps.keys())
            for item in items:
                if item in txn:
                    temp.append(item)
            ois.append(temp)
        print('\nThe ordered item sets are:')
        print(ois)
        return ois

    #generation of frequent itemsets

    def generate_freq_itemsets():
        def gen_cpb(keys,branch,node):
            try:
                branch[node.value].append((keys,node.count))
            except:
                branch[node.value] = [(keys,node.count)]
            for child in node.childs:
                gen_cpb(keys+[node.value],branch,child)
            return

        cpb = {}
        for i in range(len(fpt.childs)):
            branch = {}
            node = fpt.childs[i]
            key = [node.value]
            for child_node in node.childs:
                gen_cpb(key,branch,child_node)
            for k,v in branch.items():
                try:
                    cpb[k].append(v)
                except:
                    cpb[k] = [v]

        print('\nThe conditional pattern base is:')
        print(cpb)

        def list_intersection(l1,l2):
            return [item for item in l1 if item in l2]


        cfpt = {}
        for key,v in cpb.items():
            for i in range(len(v)):
                temp = {}
                items_visited = []
                for j in range(len(v[i])):
                    for item in v[i][j][0]:
                        if item not in items_visited:
                            count = v[i][j][1]
                            items_visited.append(item)
                            for k in range(j+1,len(v[i])):
                                if item in v[i][k][0]:
                                    count += v[i][k][1]
                            if count>=MIN_SUPPORT:
                                temp[item] = count
                try:
                    cfpt[key].append(temp)
                except:
                    cfpt[key] = [temp]
        print('\nThe conditional frequent pattern tree is:')
        print(cfpt)


        fis = {}
        for key,value in cfpt.items():
            for i in range(len(value)):
                items = list(value[i].keys())
                for j in range(1,len(items)+1):
                    itemsets = list(combinations(items,j))
                    for itemset in itemsets:
                        support = 99999999999
                        for k in itemset:
                            support = min(support,cfpt[key][i][k])
                        dict_key = tuple(sorted(list(itemset)+[key]))
                        try:
                            fis[dict_key] += support
                        except:
                            fis[dict_key] = support
        print("\nThe frequent itemset is:")
        print(fis)

    class Trie:
        def __init__(self,value=None,isWordEnd=False, count =1):
            self.value = value
            self.count = count
            self.childs = []
            self.isEndOfWord = isWordEnd
            self.parent = None
            
        def add_item(self,index,items,main_node):
            isWordEnd = index == len(items)-1
            if len(main_node.childs) == 0:
                new_node = Trie(items[index],isWordEnd)
                main_node.childs.append(new_node)
                new_node.parent = main_node
                if not isWordEnd:
                    self.add_item(index+1,items,new_node)
                return
            item_added = False
            for node in main_node.childs:
                if node.value == items[index]:
                    node.count += 1
                    if isWordEnd:
                        node.isEndOfWord = isWordEnd
                        return
                    self.add_item(index+1,items,node)
                    item_added = True
                    break
            if not item_added:
                new_node = Trie(items[index],isWordEnd)
                main_node.childs.append(new_node)
                new_node.parent = main_node
                if not isWordEnd:
                    self.add_item(index+1,items,new_node)
                return
            
    ois = get_ordered_itemset('retail_dataset.csv')
    print('\nThe frequent pattern sets are:')
    print(fps)
    fpt = Trie()

    for items in ois:
        fpt.add_item(0,items,fpt)
    print('\n Initial frequent itemsets are:')
    generate_freq_itemsets()

    #reading from new data
    new_ois = get_ordered_itemset('splitted_new.csv')
    new_fps= {}
    for item in sorted(fps.items(),key=lambda kv:(kv[1]),reverse=True):
        new_fps[item[0]] = item[1]
    fps = new_fps
    print('\nThe frequent pattern sets are:')
    print(fps)


    # adjusting


    def sort_acc_new_order(parents, items):
        new_parents=[]
        for it in items:
            if it in parents:
                new_parents.append(it)
        return new_parents

    def split(root, items, parents, min_freq, m_node):
        min_freq= min(min_freq, root.count)
        if len(root.childs)>0:
            new_parents = parents
            new_parents.append(root.value)
            for child in root.childs:
                split(child,items, new_parents, min_freq, m_node)
        else:
            ordered_parents = sort_acc_new_order(parents, items)
            for nodd in ordered_parents:
                tem = Trie(nodd, False, min_freq)
                m_node.childs.append(tem)
                m_node=tem

    def merge_stack(root1):
        stack=[]
        stack.append(root1)
        while(len(stack)>0):
            root= stack.pop()
            prev =[]
            new_childs=[]
            if len(root.childs)<=0:
                continue
            for nod in root.childs:
                if nod.value not in prev:
                    cc=0
                    new_chh=[]
                    for chh in root.childs:
                        if chh.value == nod.value:
                            cc += nod.count
                            for child in chh.childs:

                                new_chh.append(child)
                    prev.append(nod.value)
                    tem = Trie(nod.value, False, cc)
                    tem.childs= new_chh
                    new_childs.append(tem)
                    if(len(new_chh)>0):
                        stack.append(tem)
            root.childs=new_childs
    def merge(root):
        prev =[]
        new_childs=[]
        if len(root.childs)<=0:
            return 
        for nod in root.childs:
            if nod.value not in prev:
                cc=0
                new_chh=[]
                for chh in root.childs:
                    if chh.value == nod.value:
                        cc += nod.count
                        for child in chh.childs:

                            new_chh.append(child)
                prev.append(nod.value)
                tem = Trie(nod.value, False, cc)
                tem.childs= new_chh
                new_childs.append(tem)
                if(len(new_chh)>0):
                    merge(tem)
        root.childs=new_childs


    def generate_freq_itemsets_new():
        def gen_cpb(keys,branch,node):
            try:
                branch[node.value].append((keys,node.count))
            except:
                branch[node.value] = [(keys,node.count)]
            for child in node.childs:
                gen_cpb(keys+[node.value],branch,child)
            return

        cpb = {}
        for i in range(len(fpt.childs)):
            branch = {}
            node = fpt.childs[i]
            key = [node.value]
            for child_node in node.childs:
                gen_cpb(key,branch,child_node)
            for k,v in branch.items():
                try:
                    cpb[k].append(v)
                except:
                    cpb[k] = [v]
        c=1000
        for i in cpb:
            c -=1
            if(c==0):
                break
            print(i, end =' ')

    m_node = Trie()
    items = list(fps.keys())
    parents=[]
    split(fpt, items,parents, 9999999999999, m_node )
    merge_stack(m_node)
    for items in new_ois:
        m_node.add_item(0,items,m_node)
    fpt = m_node
    print('\n New frequent itemsets are:')
    generate_freq_itemsets_new()
    print("**************************************************************************")
    print("Total time taken:")
    print(time.process_time() - start)

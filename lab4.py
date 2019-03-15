#   Author: Ana Luisa Mata Sanchez
#   Course: CS2302
#   Assignment: Lab #4
#   Instructor: Olac Fuentes
#   Description: B tree operations
#   T.A.: Anindita Nath
#   Last modified: 03/15/2019
#   Purpose: Compute the height of the tree, extract the B-tree into a sorted list,
#   minimum and maximum element in the tree at depth, number of nodes in the tree at depth d,
#   print all the items at depth d,number of nodes nad leaves that are full, and return the depth of a given item.

# Code to implement a B-tree 
# Programmed by Olac Fuentes
# Last modified February 28, 2019

import math

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
        
###################################### START OF MY CODE ######################################

def btreeToList(T,A):
    if T.isLeaf:
        for i in range(len(T.item)):
            A.append(T.item[i])
    else:   
        for i in range(len(T.item)):
            print(i)
            btreeToList(T.child[i],A)           
            A.append(T.item[i])
        btreeToList(T.child[len(T.item)],A) 
    return L

def MinAtDepth(T,d):
    if d>height(T) :
        return math.inf
    if d ==0 :
        return T.item[0]
    
    return MinAtDepth(T.child[0],d-1)   

def MaxAtDepth(T,d):
    if d>height(T) :
        return math.inf
    if d ==0 :
        return T.item[-1]
    
    return MaxAtDepth(T.child[len(T.child)-1],d-1)

def NumNodesAtDepth(T,d):
    if d>height(T): 
        return math.inf
    if d == 0 :
        return 1
    if T.isLeaf:
        return 0
    count = 0
    for i in range (len(T.child)):
        count += NumNodesAtDepth(T.child[i],d-1)
    return count
    
def PrintAtDepthD(T,d):
    if d == 0 :
        for j in range (len(T.item)):
            print(T.item[j], end=" ")
    for i in range (len(T.child)):
        PrintAtDepthD(T.child[i],d-1)   

def FullNodes(T):
    if IsFull(T):
        return 1
    if T.isLeaf:
        return 0
    count = 0
    for i in range (len(T.child)):
        count += FullNodes(T.child[i])
    return count

def FullLeaves(T):
    if IsFull(T) and T.isLeaf:
        return 1
    elif T.isLeaf:
        return 0
    count = 0
    for i in range (len(T.child)):
        count += FullNodes(T.child[i])
    return count

def FindDepth(T,k):
    if k in T.item:
        return 0
            
    if T.isLeaf:
        return -1
    
    d = FindDepth(T.child[FindChild(T,k)],k)
    
    if d == -1:
        return -1
    return d + 1


    
L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6]
T = BTree()    
for i in L:
    print('Inserting',i)
    Insert(T,i)
    PrintD(T,'') 
    #Print(T)
    print('\n####################################')
    
SearchAndPrint(T,60)
SearchAndPrint(T,200)
SearchAndPrint(T,25)
SearchAndPrint(T,20)

#1
print("################# Height #################")
print(height(T))
print("")
#2
print("################# Tree to sorted list #################")
A = list()
btreeToList(T,A)
print(A)
print("")
#3
print("################# Minimum element at depth d #################")
print(MinAtDepth(T,2))
print("")
#4
print("################# Maximum element at depth d #################")
print(MaxAtDepth(T,2))
print("")
#5
print("################# Number of nodes at depth d #################")
print(NumNodesAtDepth(T,2))
print("")
#6
print("################# Print all elements at depth d #################")
PrintAtDepthD(T,2)
print(" ")
#7
print("################# Full node count #################")
print(FullNodes(T))
print("")
#8
print("################# Full leaves count #################")
print(FullLeaves(T))
print("")
#9
print("################# Find depth of an item #################")
print(FindDepth(T,10))
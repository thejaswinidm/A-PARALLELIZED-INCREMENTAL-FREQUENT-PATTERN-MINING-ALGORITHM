# A-PARALLELIZED-INCREMENTAL-FREQUENT-PATTERN-MINING-ALGORITHM
Motivation\
The rapid increase in the amount of data in this big data era has lead to proposal of many approaches to solve the incremental problem of certain data, but these approaches did not address uncertain data
There is a need for a method to retain the tree structure in uncertain data, to maintain the flexibility of the original data, and should not require to rebuild the tree again.\
# Method description
1.Constructing the original tree\
2.Updating the accumulation table and tree based on the new transactions added\
3.Adding the new transactions to the original tree and obtaining the frequent patterns\

# 1.Constructing the original tree
a. Constructing accumulation table
b. Sorting the items according to their probabilities in transactions record
c. Sorting the transactions
d. Constructing the tree
e. Identifying the frequent patterns

# homework 1
>Hint 1: Implement delete(key)

>Hint 2: Implement rehashing

>Hint 3: Improve the hash function

- changed the hash calculation so that hash do not collide
```
for each character in the string
    hash = hash * 31 + character
```

- done in hash_table.py
- added a new funciton in class HashTable to resize the table
    - if the load factor is greater than 0.7, resize the table to double the size

# homework 2
> The complexity of searching / adding / removing an element is mostly O(1) with a hash table, whereas the complexity is O(log N) with a tree. This means that a hash table is more efficient than a tree. However, real-world large-scale database systems tend to prefer a tree to a hash table. Why? List as many reasons as possible.

### Answer
1. **Hash table is not good at range queries.**  
    - Hash table is good at searching for a specific key, but it is not good at range queries. For example, if you want to find all the keys between 1 and 100, you have to search for each key one by one. On the other hand, a tree can easily find all the keys between 1 and 100 by traversing the tree.
2. **Hash table needs resizing and when there are many data inside the hash table, recalculating the hash will cost much calculation**
    - Whereas in a tree, the size can be grown without resizing nor recalculation of all hash values, but only a few
    - the database cannot be used while the resize is done
3. **The calculation of hash becomes more time consuming depending on the amount of data**
    - The more data there are in the hash table, the calculation of hash becomes more constly in order not to have too much collision

# homework 3
> Design a cache that achieves the following operations with mostly O(1)
When a pair of <URL, Web page> is given, find if the given pair is contained in the cache or not
If the pair is not found, insert the pair into the cache after evicting the least recently accessed pair

## what a cash does (brainstorming below)
### 1.checks whether the <url, web page> exists in the table

### 2a. if exists, 

then bring the link to the top

the order of url before the found url must be added by one

### 2b. if not exist,

then remove the end url

add the url searched at the top 

all the others' orders must be added by one 

- the data structure must be some kind of graph that does not need index altering for data when data is deleted at the end
- also, the data structure must be some kind of graph that does not need index altering when data is inserted at the start
- also, the data must allow deleting item from somewhere in middle of the structure with O(1)
    - or not delete, however, move the item in the middle to the top in O(1)
- otherwise, the O(1) cannot be achieved
- sounds like a LIFO data structure

### The way to do this 

1. create a hash table that contains the hash of the url and node address as a value
2. create a doubly linked list with nodes in the order of the most recently used at the top and least recently used at the bottom

# homework 4
> Design a cache that achieves the following operations with mostly O(1)
When a pair of <URL, Web page> is given, find if the given pair is contained in the cache or not
If the pair is not found, insert the pair into the cache after evicting the least recently accessed pair

- done in cache.py
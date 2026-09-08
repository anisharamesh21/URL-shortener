class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity:int):
        self.capacity = capacity
        self.cache = {} ## empty hashmap
        self.head = Node(0,0) ## dummy head
        self.tail = Node (0,0) ## dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev_node = node.prev
        prev_node.next = node.next
        next_node = node.next
        next_node.prev = node.prev
       
    def _add_to_front(self, node):
        next_node = self.head.next
        self.head.next = node
        node.next = next_node
        node.prev = self.head
        next_node.prev = node

    def get(self, key:int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return -1
    
    def put(self, key:int, value:int) -> None:
        if key in self.cache:
            existing_node = self.cache[key]
            self._remove(existing_node)
        new_node = Node(key, value)
        self.cache[key]= new_node
        self._add_to_front(new_node)
        if len(self.cache)>self.capacity:
            least_used = self.tail.prev
            self._remove(least_used)
            del self.cache[least_used.key]


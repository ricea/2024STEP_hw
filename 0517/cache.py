# a node to save the url in a doubly linked list
class Node:
    def __init__(self, url, page):
        self.url = url
        self.page = page
        self.prev = None
        self.next = None

# cache
class Cache:
    def __init__(self, size):
        self.size = size
        self.dict = {}
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_to_head(self, node):
        now_head = self.head.next
        node.prev = self.head
        node.next = now_head
        now_head.prev = node
        self.head.next = node

    def remove_from_tail(self):
        if self.tail.prev != self.head:
            node_to_rm = self.tail.prev
            self.remove_from_dict(node_to_rm)
            del self.dict[node_to_rm.url]
    
    def put(self, url, page):
        if url in self.dict:
            node = self.dict[url]
            self.remove_from_dict(node)
        else:
            node = Node(url, page)
            self.dict[url] = node
            if len(self.dict) > self.size:
                self.remove_from_tail()
        self.add_to_head(node)

    def get(self, url):
        if url in self.dict:
            node =self.dict[url]
            self.remove_from_dict(node)
            self.add_to_head(node)
            return node.page
        return None

    def remove_from_dict(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def contains(self, url):
        return url in self.dict

# Example usage
lru_cache = Cache(size=3)
lru_cache.put("http://example.com", "<html>Example</html>")
print([node.url for node in lru_cache.dict.values()])  # Check the order of URLs
lru_cache.put("http://example.org", "<html>Example Org</html>")
print([node.url for node in lru_cache.dict.values()])  # Check the order of URLs
print(lru_cache.contains("http://example.com"))  # Should return True
print([node.url for node in lru_cache.dict.values()])  # Check the order of URLs
print(lru_cache.get("http://example.com"))  # Should return "<html>Example</html>"
lru_cache.put("http://example.net", "<html>Example Net</html>")
print([node.url for node in lru_cache.dict.values()])  # Check the order of URLs
lru_cache.put("http://example.info", "<html>Example Info</html>")
print([node.url for node in lru_cache.dict.values()])  # Check the order of URLs
print(lru_cache.contains("http://example.org"))  # Should return False (evicted)
print(lru_cache.get("http://example.com"))  # Should return "<html>Example</html>"
print(lru_cache.get("http://example.info"))  # Should return "<html>Example Info</html>"
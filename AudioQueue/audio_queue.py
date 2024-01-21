class AudioQueue:
    def __init__(self, max_size):
        self.queue = []
        self.max_size = max_size

    def enqueue(self, item):
        if len(self.queue) < self.max_size:
            self.queue.append(item)
        else:
            print("Queue is full. Cannot enqueue more items.")

    def dequeue(self):
        if self.is_empty():
            print("Queue is empty. Cannot dequeue.")
        else:
            return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return len(self.queue) == self.max_size

    def size(self):
        return len(self.queue)
    
    def empty_queue(self):
        self.queue = []  # Clears all items from the queue
    
    def __str__(self):
        return f"AudioQueue: {self.queue}"
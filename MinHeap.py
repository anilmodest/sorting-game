import heapq


class MinHeap:
    def __init__(self, ):
        self.heap = []

    def push(self, distance, item):
        #self.heap.append((distance, item));
        # print('--print heap inputs----')
        # print(*self.heap, sep=", ")
        # print(item)
        # print(distance)
        # print('------')
        entry = [distance, item];
        heapq.heappush(self.heap, entry)

    def pop(self):

        priority,  item = heapq.heappop(self.heap);
        return item;

    def __len__(self):
        return len(self.heap)




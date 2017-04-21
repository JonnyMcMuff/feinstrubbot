class myIterator:
    def __init__(self, handler_list):
        self.handler_list = handler_list
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        number_of_items = len(self.handler_list)
        if self.counter >= number_of_items:
            self.counter = 0
            raise StopIteration
        else:
            current_item = self.handler_list[self.counter]
            self.counter += 1
            return current_item




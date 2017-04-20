class FeinstrubHelper:
    def __init__(self):
        pass

    def is_Float(self,value):
        try:
            float(value)
            return True
        except:
            return False

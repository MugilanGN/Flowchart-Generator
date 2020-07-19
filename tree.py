class newNode: 
    def __init__(self, data): 
        self.data = data  
        self.left = self.right = None  

class newTree:
    def __init__(self, arr, insertType):
        self.root = None
        self.serialBuffer = []
        if insertType == "levelorder":
            self.insertLevelOrder(arr, 0, len(arr))
        
    def insertLevelOrder(self, arr, start, end): 
        if start < end:
            temp = newNode(arr[start])
            if self.root == None:
                self.root = temp
            temp.left = self.insertLevelOrder(arr, 2 * start + 1, end)  
            temp.right = self.insertLevelOrder(arr, 2 * start + 2, end)
            return temp
        else:
            return None
        
    def serializeInOrder(self, root):
        if root != None:
            self.serializeInOrder(root.left)
            self.serialBuffer.append(root.data)
            self.serializeInOrder(root.right)
        return self.serialBuffer
    
    def printInOrder(self, root):
        if root != None:
            self.printInOrder(root.left)
            print(root.data)
            self.printInOrder(root.right)

if __name__ == '__main__':
    tree = newTree([0,1,2,3],"levelorder")

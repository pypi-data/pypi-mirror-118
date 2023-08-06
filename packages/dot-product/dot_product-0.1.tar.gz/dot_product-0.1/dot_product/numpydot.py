import numpy as np

class DotProduct:
    def dot_product(self,a,b):
        try:
            res= np.dot(a,b)
            return res
        except:
            print("The shape of array is not matching")
        
            
if __name__=="__main__":
    a = np.array([2,3,8])
    b = np.array([3,4,5])
    dot = DotProduct()
    c = dot.dot_product(a,b)
    print(f'value of c {c}')


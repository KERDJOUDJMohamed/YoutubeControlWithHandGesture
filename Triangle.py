from math import sqrt

class Point :
    def __init__(self, x : int , y : int):
        """Creat a Point Object -> Point(int :x , int :y)"""
        self.x = x
        self.y = y  
        
    def Display(self):
        """Display coordinate point of a point"""
        print("({},{})".format(self.x,self.y))

class Line:
    @staticmethod
    def near(p1 : Point , p2 : Point , error = 25):
        """Return true if one point is near to the other , false otherwise , takes : point 1 , point 2 , error in pixel """
        distance = Triangle.Distance(p1,p2)
        if distance <= error : 
            #print("Mouse Draging!")
            return True 
        #print("Mouse Relesed!")
        return False

class Triangle:
    def __init__(self,p1 : Point , p2 : Point , p3 : Point):
        """Create Triange of 3 Points"""
        self.p1 = p1
        self.p2 = p2 
        self.p3 = p3
        self.p1p2 = Triangle.Distance(p1,p2)
        self.p2p3 = Triangle.Distance(p2,p3)
        self.p1p3 = Triangle.Distance(p1,p3)
        self.s =  (self.p1p2 + self.p2p3 + self.p1p3)/2
        self.A = self.Area()
    
    def Area(self):
        """Return the Area of a Triangle"""
        num = (self.s*(self.s-self.p1p2)*(self.s-self.p1p3)*(self.s-self.p2p3))**0.5
        try :
            num = round(num)
        except:
            pass
        return num
        
    @staticmethod
    def Distance(p1 : Point , p2 : Point):
        """Return the Distance between 2 Points"""
        return round(sqrt((( p1.x - p2.x )** 2) + ((p1.y - p2.y)**2)),2) 

    def In(self,p : Point):
        tr1 = Triangle(self.p1,self.p2,p).Area()
        tr2 = Triangle(self.p1,self.p3,p).Area()
        tr3 = Triangle(self.p2,self.p3,p).Area()
        if tr1 + tr2 + tr3 == self.A : 
            return True
        else :
            return False
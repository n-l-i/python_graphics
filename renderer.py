
# Imports each and every method and class 
# of module tkinter and tkinter.ttk 
import tkinter,time

class Window():
    def __init__(self,width,height):
        self.height = height
        self.width = width
        self.x_position = 100
        self.y_position = 300
        self.root = tkinter.Tk()
        self.root.geometry(str(self.width)+"x"+str(self.height)+"+"+str(self.x_position)+"+"+str(self.y_position))

        self.canvas = tkinter.Canvas(self.root,height=self.height,width=self.width)
        self.canvas.pack()

    def update(self):
        self.root.update()
        
    def close(self):
        self.root.destroy()
    
    def create_rectangle(self,x1y1,x2y2,colour):
        attributes = {"fill":colour,
                   "outline":colour}
        (x1,y1)=x1y1
        (x2,y2)=x2y2
        return self.canvas.create_rectangle(x1,y1,x2,y2,attributes)
    
    def update_rectangle(self,rectangle_id,colour):
        attributes = {"fill":colour,
                   "outline":colour}
        self.canvas.itemconfigure(rectangle_id, attributes)

class Rectangle():
    def __init__(self,window,x1,y1,x2,y2,colour="black"):
        self.window = window
        self.x1y1=(x1,y1)
        self.x2y2=(x2,y2)
        self.colour = colour
        self.rectangle_id = None
        
    def draw(self):
        self.rectangle_id = self.window.create_rectangle(self.x1y1,self.x2y2,self.colour)
        
    def set_colour(self,colour):
        self.colour = colour
        self.window.update_rectangle(self.rectangle_id, self.colour)

        

#test

w = Window(300,300)
t=[]
for i in range(0,10):
    t.append(Rectangle(w,i*40,0,40+i*40,40))

for i in range(10):
    t[i].draw()
    w.update()
    time.sleep(0.1)
    

for i in range(10):
    t[i].set_colour("red")
    t[i].draw()
    w.update()
    time.sleep(0.1)

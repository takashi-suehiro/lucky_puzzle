from tkinter import *
from math import *
import pickle

# allows moving dots with multiple selection. 

FIX_COLOR = "blue"
MOVE_COLOR = "green"
UNSELECTED_COLOR = "green"
SELECTED_COLOR = "red"

class Test(Frame):
    ###################################################################
    ###### Event callbacks for THE CANVAS (not the stuff drawn on it)
    ###################################################################
    def mouseDown(self, event):
        # see if we're inside a dot. If we are, it
        # gets tagged as CURRENT for free by tk.
        c_items = event.widget.find_withtag(CURRENT)
        if not c_items :
            # we clicked outside of all dots on the canvas. unselect all.
            
            # re-color everything back to an unselected color
            self.draw.itemconfig("selected", fill=UNSELECTED_COLOR)
            # unselect everything
            self.draw.dtag("selected")
        else:
            tmp = self.draw.gettags(c_items[0])
#            print( tmp)
            # mark as "selected" the thing the cursor is under
            if "move" in tmp :
              self.draw.addtag("selected", "withtag", CURRENT)
              # color it as selected
              self.draw.itemconfig("selected", fill=SELECTED_COLOR)
            else :
              self.draw.itemconfig("selected", fill=UNSELECTED_COLOR)
              self.draw.dtag("selected")
              self.coordsParts(self.parts[tmp[0]]["move"],
                               self.parts[tmp[0]]["v"])

        self.lastx = event.x
        self.lasty = event.y

    def coordsParts(self,id,coords) :
        if len(coords) == 6 :
          self.draw.coords(id,
                           coords[0],coords[1],
                           coords[2],coords[3],
                           coords[4],coords[5])
        elif len(coords) == 8 :
          self.draw.coords(id,
                           coords[0],coords[1],
                           coords[2],coords[3],
                           coords[4],coords[5],
                           coords[6],coords[7])
        elif len(coords) == 10 :
          self.draw.coords(id,
                           coords[0],coords[1],
                           coords[2],coords[3],
                           coords[4],coords[5],
                           coords[6],coords[7],
                           coords[8],coords[9])

    def mouseDownR(self, event):
        self.lastx = event.x
        self.lasty = event.y
        self.centerx = event.x
        self.centery = event.y
  
    def mouseDownM(self, event):
        self.lastx = event.x
        self.lasty = event.y
        tmp = self.draw.find_withtag("selected")
#       print( tmp)
        for tmp0 in tmp :
          tmp1 = self.draw.coords(tmp0)
#          print( tmp1)
          tmp2 = []
          tmp3 = len(tmp1)/2
          for i in range(tmp3) :
            tmpx = 2 * event.x - tmp1[2*i]
            tmpy = tmp1[2*i +1]
            tmp2.append(tmpx)
            tmp2.append(tmpy)
#         print( tmp2)
#         self.draw.coords("selected", tmp2)
          self.coordsParts(tmp0,tmp2)

        
    def mouseMove(self, event):
        self.draw.move("selected", event.x - self.lastx, event.y - self.lasty)
        self.lastx = event.x
        self.lasty = event.y


    def mouseRotate(self, event):

        if event.x > self.centerx and event.y < self.centery :
          cx = cos((event.x - self.lastx + event.y - self.lasty)/100.0)
          sx = sin((event.x - self.lastx + event.y - self.lasty)/100.0)
        elif event.x < self.centerx and event.y < self.centery :
          cx = cos((event.x - self.lastx - event.y + self.lasty)/100.0)
          sx = sin((event.x - self.lastx - event.y + self.lasty)/100.0)
        elif event.x < self.centerx and event.y > self.centery :
          cx = cos((- event.x + self.lastx - event.y + self.lasty)/100.0)
          sx = sin((- event.x + self.lastx - event.y + self.lasty)/100.0)
        else:
          cx = cos((- event.x + self.lastx + event.y - self.lasty)/100.0)
          sx = sin((- event.x + self.lastx + event.y - self.lasty)/100.0)

#        tmpx = event.x - self.lastx
#        tmpy = event.y - self.lasty
#        tmpr = sqrt(tmpx * tmpx + tmpy * tmpy)
#        cx = tmpx / tmpr
#        sx = tmpy / tmpr
        tmp = self.draw.find_withtag("selected")
#       print( tmp)
        for tmp0 in tmp :
          tmp1 = self.draw.coords(tmp0)
#          print( tmp1)
          tmp2 = []
          tmp3 = int(len(tmp1)/2)
          for i in range(tmp3) :
            tmpx = tmp1[2*i] - self.centerx
            tmpy = tmp1[2*i +1] - self.centery
            tmp2.append(self.centerx + cx * tmpx - sx * tmpy)
            tmp2.append(self.centery + sx * tmpx + cx * tmpy)
#         print( tmp2)
#         self.draw.coords("selected", tmp2)
          self.coordsParts(tmp0,tmp2)
        self.lastx = event.x
        self.lasty = event.y

    def printState(self):
#        print( self.parts)
        for tmp in self.parts.keys() :
          print( tmp, self.draw.coords(self.parts[tmp]["move"]))

    def saveState(self):
        data = {}
        for tmp in self.parts.keys() :
           data[tmp] = self.draw.coords(self.parts[tmp]["move"])
        svfile = open("lucky.sav","w")
        pickle.dump(data,svfile)
        svfile.close()

    def loadState(self):
        svfile = open("lucky.sav")
        data = pickle.load(svfile)
        svfile.close()
        for tmp in data.keys() :
           self.coordsParts(self.parts[tmp]["move"],data[tmp])

    def createItems(self):
        for i in self.parts.keys():
          self.parts[i]["fix"] = self.draw.create_polygon(self.parts[i]["v"],
                                     fill=FIX_COLOR,
                                     outline="black",
                                     tags=(i))
        for i in self.parts.keys():
          self.parts[i]["move"] = self.draw.create_polygon(
                                     self.parts[i]["v"][:],
                                     fill=MOVE_COLOR,
                                     outline="black",
                                     tags=(i,"move"))

    def createWidgets(self):
        ################
        # make the canvas and bind some behavior to it
        ################
        self.draw = Canvas(self, width="5i", height="5i")
        Widget.bind(self.draw, "<1>", self.mouseDown)
        Widget.bind(self.draw, "<2>", self.mouseDownM)
        Widget.bind(self.draw, "<Shift-1>", self.mouseDownM)
        Widget.bind(self.draw, "<3>", self.mouseDownR)
        Widget.bind(self.draw, "<B1-Motion>", self.mouseMove)
        Widget.bind(self.draw, "<B3-Motion>", self.mouseRotate)

        # and other things.....
        f = Frame(self, relief=GROOVE, bd=3)
        self.QUIT = Button(f, text='QUIT', foreground='red',
                           command=self.quit)

        self.button1 = Button(f, text="print", foreground="blue",
                             command=self.printState)
        self.button2 = Button(f, text="save", foreground="blue",
                             command=self.saveState)
        self.button3 = Button(f, text="load", foreground="blue",


#       self.button1 = Button(self, text="print", foreground="blue",
#                            command=self.printState)
#       self.button2 = Button(self, text="save", foreground="blue",
#                            command=self.saveState)
#       self.button3 = Button(self, text="load", foreground="blue",
                             command=self.loadState)

#       message = ("%s parts are selected and can be dragged.\n"
#                  "%s are not selected.\n"
#                  "Click in a dot to select it.\n"
#                  "Click on empty space to deselect all dots."
#                  ) % (SELECTED_COLOR, UNSELECTED_COLOR)
        message = (

       "left-click in a green piece to select it to be moved. "
       "the selected piece turns red.\n"
       "continuing left-clicks in other green pieces "
       "to select other pieces.\n"
       "left-click on empty space to deselect all pieces.\n"
       "left-drag on selected pieces to translation of them.\n"
      "right-drag to rotation of the selected pieces.\n"
      "center-click or shift-left-clicks to turn the selected pieces.\n"
      "blue shows the original places. left-click on a blue piece "
      "to return the corresponding green piece."
                   )
        self.label = Message(self, width="5i", text=message)


#       self.QUIT.pack(side=BOTTOM, fill=BOTH)
        self.label.pack(side=BOTTOM, fill=X, expand=1)
        self.QUIT.pack(side=LEFT, fill=BOTH)
        self.button1.pack(side=LEFT, fill=X)
        self.button2.pack(side=LEFT, fill=X)
        self.button3.pack(side=LEFT, fill=X)
        f.pack(side=BOTTOM, fill=X)
#       self.button1.pack(side=BOTTOM, fill=X)
#       self.button2.pack(side=BOTTOM, fill=X)
#       self.button3.pack(side=BOTTOM, fill=X)
        self.draw.pack(side=LEFT)
       
    def mul_unit(self,x):
        return(self.unit * x)

    def init(self) :
        self.master.title("Lucky Puzzle")
        # define parts
        self.unit = 30
        self.v_tri1 = list(map(self.mul_unit,[0,0,2,0,0,2]))
        self.v_tri2 = list(map(self.mul_unit,[2,0,4,0,4,2]))
        self.v_nife1 = list(map(self.mul_unit,[0,2,2,0,3,1,0,4]))
        self.v_nife2 = list(map(self.mul_unit,[2,2,3,1,4,2,4,4]))
        self.v_nife3 = list(map(self.mul_unit,[0,4,1,3,1,5,0,5]))
        self.v_nife4 = list(map(self.mul_unit,[3,3,4,4,4,5,3,5]))
        self.v_house = list(map(self.mul_unit,[1,3,2,2,3,3,3,5,1,5]))
        self.parts = {}
        self.parts["tri1"] = {"v":self.v_tri1}
        self.parts["tri2"] = {"v":self.v_tri2}
        self.parts["nife1"] = {"v":self.v_nife1}
        self.parts["nife2"] = {"v":self.v_nife2}
        self.parts["nife3"] = {"v":self.v_nife3}
        self.parts["nife4"] = {"v":self.v_nife4}
        self.parts["house"] = {"v":self.v_house}
        self.createWidgets()
        self.createItems()

#    def pack() :
#       Pack.config(self)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.init()



test = Test()
test.mainloop()

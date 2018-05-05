'''
started 30/04/2018

'''

import random, tkinter, time

class game(object):
    def __init__(self, tk, canvas):
        self.tk, self.canvas = tk, canvas
        self.alive = True
        #kleuren
        self.colors = {2:'#08ed15' ,4:'#9f3396', 8:'#00962a', 16:'#55a2ac', \
                    32:'#ab1255', 64:'#ffff00', 128:'#00ffff', 256:'#ff00ff', \
                    512:'#ffa500', 1024:'#ff0000', 2048:'#00ff9f'}
        self.nummers = [0] * 16
        #om te beginnen moeten ze gewoon verschillen
        self.oud = None
        self.draw()
        



        
        self.canvas.bind_all('<KeyPress - Left>', self.move_left)
        self.canvas.bind_all('<KeyPress - Right>', self.move_right)
        self.canvas.bind_all('<KeyPress - Up>', self.move_up)
        self.canvas.bind_all('<KeyPress - Down>', self.move_down)

    def move_left(self, evt):
        #stadaard
        self.oud = self.nummers.copy()
        for i in range(0,15,4):
             tta = self.combine(self.shift(self.nummers[i:i+4]))
             self.nummers[i:i+4] = self.shift(tta)
        self.draw()
          
        
    def move_right(self, evt):
        #we vormen eerst alles om naar een linkse rotatie en dan terug
        #Kon via splicing :( nog niet optimaal
        self.oud = self.nummers.copy()
        calc = 16*[0]
        for reeks in range(0,16,4):
            for j in range(3,-1,-1):
                calc[reeks+j] = self.nummers[reeks+3-j]
                   
            calc[reeks:reeks+4] = self.shift(self.combine(self.shift( \
                calc[reeks:reeks+4])))
            for j in range(3,-1,-1):
                self.nummers[reeks+3-j] = calc[reeks + j]
        self.draw()
        

    def move_up(self, evt):

        self.oud = self.nummers.copy()
        for i in range(4):
            kolom = self.nummers[i:16:4]
            self.nummers[i:16:4] =  self.shift(self.combine(self.shift(kolom)))
        self.draw()

    def move_down(self, evt):

        self.oud = self.nummers.copy()

        for i in range(12,16):
            kolom = self.nummers[i:3:-4] + [self.nummers[i-12]]
            ber = self.shift(self.combine(self.shift(kolom)))
            self.nummers[i:3:-4] = ber[:3]
            self.nummers[i-12] = ber[3]
        
        self.draw()
        
                
    def draw(self):
        
        i = self.nummers.count(0)
        if i == 0:
            print('game over')
            self.alive = False
            return
        if self.oud == self.nummers:
            return

        mogloc = []
        for i in range(0, 16):
            if self.nummers[i] == 0:
                mogloc.append(i)
        self.nummers[random.choice(mogloc)] = 2 + 2*(random.random()>0.5)
    
        self.canvas.delete('all')
        for j in range(4):
            for i in range(4):
                x = self.canvas.create_rectangle(i*50, j*50, (i+1)*50, (j+1)*50)
                if self.nummers[j*4+i] == 0:
                    continue
                self.canvas.create_text(25+i*50, 25+j*50, anchor=tkinter.CENTER, \
                    text=str(self.nummers[j*4+i]), font=('Helvetica', 15))
                self.canvas.itemconfig(x, fill=self.colors.get(\
                    self.nummers[j*4+i], 'white'))
        #print('a',self.nummers)
        
        
    def shift(self, k):
        while 0 in k:
            k.remove(0)
        return k + [0]*(4-len(k))

    def combine(self, k):
        for i in range(3):
            if k[i] == k[i+1]:
                k[i] = k[i]*2
                k[i+1] = 0
        return k
                
        


tk = tkinter.Tk()
tk.resizable(0,0)
tk.title('2048')
tk.wm_attributes('-topmost', 1)
canvas = tkinter.Canvas(tk, width=201, height=201, bd=0, highlightthickness=0)
canvas.pack()
k = game(tk, canvas)

while k.alive:
    tk.update()
    tk.update_idletasks()

time.sleep(2)
tk.destroy()
    

    


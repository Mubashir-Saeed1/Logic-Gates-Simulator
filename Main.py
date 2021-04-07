import pygame, tktext
from gates import *

# declarations

red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
orange = (255,200,100)
white = (255,255,255)
screen = pygame.display.set_mode([1200,700])
img="dummy.jpg"
d={'and':'and.png',"":'dummy.png','or':'or.png','nor':'nor.png','not':'not.png','nand':'nand.png','xor':'xor.png','delete':'delete.jpg', 'FA':'fulladder.jpg','HA':'halfadder.jpg','xnor':'xnor.png'}
gates_dict = dict()
gate_counter = 0
graph = []
clickedgate=""
event=pygame.event.poll()
pos1=(30,30)
socket_clicked = False
points_list=[]
lines = []
socket1 = None
socket2 = None
button_clicked = False
mouse_click_points = []
delete_set = False
buttons_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_gates = pygame.sprite.Group()
save_list = pygame.sprite.Group()
socket_list = pygame.sprite.Group()
help_list = pygame.sprite.Group()

# ----------------------------------------------------------------------------------------------------------------------------------------------- #

#class to create gates
class Gates(pygame.sprite.Sprite):
    def __init__(self,gate):
         pygame.sprite.Sprite.__init__(self)
         self.gatetype=gate
         self.noneexists = False
         global d, all_sprites, gates_dict, gate_counter, points_list, graph
         img = pygame.image.load(d[gate])
         self.image = img.convert()
         self.image.set_colorkey(white)      
         self.rect = self.image.get_rect()
         if(gate!='not'): # because all other gates have two sockets
             gates_dict[gate_counter] = self
             gate_counter += 1

             if(gate=='HA'):
                 self.outputSocket = [Socket('out',self), Socket('out',self)]
                 self.inputSockets = [Socket('in', self), Socket('in', self)]
             elif(gate == 'FA'):
                 self.outputSocket = [Socket('out',self), Socket('out',self)]
                 self.inputSockets = [Socket('in', self), Socket('in', self), Socket('in', self)]
             else:
                 self.inputSockets = [Socket('in', self), Socket('in', self)]
                 self.outputSocket = Socket('out', self)
             
         elif(gate=='not'):
             gates_dict[gate_counter] = self
             gate_counter += 1
             self.inputSockets = [Socket('in',self)]
             self.outputSocket = Socket('out',self)
             
#........................................................................................................................................... #
             
    def draw_socket(self):
        # to draw sockets on each input and output of the gate
        if(self.gatetype != 'not'):
            if(self.gatetype == 'FA'):
                self.inputSockets[0].rect.x = (self.rect.x)-1
                self.inputSockets[0].rect.y = (self.rect.y)+24
                all_sprites.add(self.inputSockets[0])
                socket_list.add(self.inputSockets[0])
                self.inputSockets[1].rect.x = (self.rect.x)-1
                self.inputSockets[1].rect.y = (self.rect.y)+55
                all_sprites.add(self.inputSockets[1])
                socket_list.add(self.inputSockets[1])
                self.inputSockets[2].rect.x = (self.rect.x)-1
                self.inputSockets[2].rect.y = (self.rect.y)+87
                all_sprites.add(self.inputSockets[2])
                socket_list.add(self.inputSockets[2])
                self.outputSocket[0].rect.x = (self.rect.x)+181
                self.outputSocket[0].rect.y = (self.rect.y)+34
                all_sprites.add(self.outputSocket[0])
                socket_list.add(self.outputSocket[0])
                self.outputSocket[1].rect.x = (self.rect.x)+181
                self.outputSocket[1].rect.y = (self.rect.y)+77
                all_sprites.add(self.outputSocket[1])
                socket_list.add(self.outputSocket[1])
                
            elif(self.gatetype == 'HA'):
                self.inputSockets[0].rect.x = (self.rect.x)-1
                self.inputSockets[0].rect.y = (self.rect.y)+19
                all_sprites.add(self.inputSockets[0])
                socket_list.add(self.inputSockets[0])
                self.inputSockets[1].rect.x = (self.rect.x)-1
                self.inputSockets[1].rect.y = (self.rect.y)+84
                all_sprites.add(self.inputSockets[1])
                socket_list.add(self.inputSockets[1])
                self.outputSocket[0].rect.x = (self.rect.x)+181
                self.outputSocket[0].rect.y = (self.rect.y)+31
                all_sprites.add(self.outputSocket[0])
                socket_list.add(self.outputSocket[0])
                self.outputSocket[1].rect.x = (self.rect.x)+181
                self.outputSocket[1].rect.y = (self.rect.y)+74
                all_sprites.add(self.outputSocket[1])
                socket_list.add(self.outputSocket[1])

            else:
                self.inputSockets[0].rect.x = (self.rect.x)-1
                self.inputSockets[0].rect.y = (self.rect.y)+12
                all_sprites.add(self.inputSockets[0])
                socket_list.add(self.inputSockets[0])
                self.inputSockets[1].rect.x = (self.rect.x)-1
                self.inputSockets[1].rect.y = (self.rect.y)+33
                all_sprites.add(self.inputSockets[1])
                socket_list.add(self.inputSockets[1])
                self.outputSocket.rect.x = (self.rect.x)+95
                self.outputSocket.rect.y = (self.rect.y)+22
                all_sprites.add(self.outputSocket)
                socket_list.add(self.outputSocket)
        
        else:
            self.inputSockets[0].rect.x = self.rect.x-1
            self.inputSockets[0].rect.y = self.rect.y+22
            all_sprites.add(self.inputSockets[0])
            socket_list.add(self.inputSockets[0])
            self.outputSocket.rect.x = self.rect.x+90
            self.outputSocket.rect.y = self.rect.y+22
            all_sprites.add(self.outputSocket)
            socket_list.add(self.outputSocket)

#.......................................................................................................................................... #
                        

    def get_input_values(self): # get input values from the sockets
        if(self.gatetype!='not'):
            self.in_val1 = self.inputSockets[0].val
            self.in_val2 = self.inputSockets[1].val
        else:
            self.in_val1 = self.inputSockets[0].val

    def set_output_values(self, value): # set output value to the socket
        #self.out.val = value
        if(isinstance(value, list)):
            self.outputSocket[0].val = value[0]
            self.outputSocket[1].val = value[1]
            
            for i in self.outputSocket[0].outgoing:
                i.val = self.outputSocket[0].val
            for i in self.outputSocket[1].outgoing:
                i.val = self.outputSocket[1].val
        else:
            self.outputSocket.val = value
            for i in self.outputSocket.outgoing:
                i.val = self.outputSocket.val

#....................................................................................................................................... #

    def delete(self):
        global gate_counter, gates_dict
        forbidden = ['not','HA','FA']
        if(self.gatetype not in forbidden):
            for i in self.outputSocket.outgoing:
                i.incoming = None
                i.connected = False
            for i in self.inputSockets:
                if(i.incoming!=None):
                    i.incoming.outgoing.remove(i)
            for i in lines: # to make lines white
                for j in i:
                    xo = self.outputSocket.rect.x
                    yo = self.outputSocket.rect.y
                    xi1 = self.inputSockets[0].rect.x
                    yi1 = self.inputSockets[0].rect.y
                    xi2 = self.inputSockets[1].rect.x
                    yi2 = self.inputSockets[1].rect.y
                    xorange = [xo+i for i in range(-4,4,1)]
                    yorange = [yo+i for i in range(-4,4,1)]
                    xi1range = [xi1+i for i in range(-4,4,1)]
                    yi1range = [yi1+i for i in range(-4,4,1)]
                    xi2range = [xi2+i for i in range(-4,4,1)]
                    yi2range = [yi2+i for i in range(-2,4,1)]

                   
                    if((j[0] in xorange or j[1] in yorange) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xi1range or j[1] in yi1range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xi2range or j[1] in yi2range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
           
        elif(self.gatetype == 'not'):
           for i in self.outputSocket.outgoing:
                i.incoming = None
                i.connected = False
           for i in self.inputSockets:
                if(i.incoming!=None):
                    i.incoming.outgoing.remove(i)
           for i in lines: # to make lines white
                for j in i:
                    xo = self.outputSocket.rect.x
                    yo = self.outputSocket.rect.y
                    xi1 = self.inputSockets[0].rect.x
                    yi1 = self.inputSockets[0].rect.y
                    xorange = [xo+i for i in range(-4,4,1)]
                    yorange = [yo+i for i in range(-4,4,1)]
                    xi1range = [xi1+i for i in range(-4,4,1)]
                    yi1range = [yi1+i for i in range(-4,4,1)]
                    
                    if((j[0] in xorange or j[1] in yorange) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xi1range or j[1] in yi1range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                        
        elif(self.gatetype == 'full'):
            for i in self.outputSocket[0].outgoing:
                i.incoming = None
                i.connected = False
            for i in self.outputSocket[1].outgoing:
                i.incoming = None
                i.connected = False
            for i in self.inputSockets:
                if(i.incoming!=None):
                    i.incoming.outgoing.remove(i)
            for i in lines: # to make lines white
                for j in i:
                    xo1 = self.outputSocket[0].rect.x
                    yo1 = self.outputSocket[0].rect.y
                    xo2 = self.outputSocket[1].rect.x
                    yo2 = self.outputSocket[1].rect.y
                    xi1 = self.inputSockets[0].rect.x
                    yi1 = self.inputSockets[0].rect.y
                    xi2 = self.inputSockets[1].rect.x
                    yi2 = self.inputSockets[1].rect.y
                    xi3 = self.inputSockets[2].rect.x
                    yi3 = self.inputSockets[2].rect.y
                    
                    xo1range = [xo1+i for i in range(-4,4,1)]
                    yo1range = [yo1+i for i in range(-4,4,1)]
                    xo2range = [xo2+i for i in range(-4,4,1)]
                    yo2range = [yo2+i for i in range(-4,4,1)]
                    xi1range = [xi1+i for i in range(-4,4,1)]
                    yi1range = [yi1+i for i in range(-4,4,1)]
                    xi2range = [xi2+i for i in range(-4,4,1)]
                    yi2range = [yi2+i for i in range(-4,4,1)]
                    xi3range = [xi3+i for i in range(-4,4,1)]
                    yi3range = [yi3+i for i in range(-4,4,1)]
                    
                    if((j[0] in xo1range or j[1] in yo1range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xo2range or j[1] in yo2range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xi1range or j[1] in yi1range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xi2range or j[1] in yi2range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xi3range or j[1] in yi3range) and (self ==i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)

        elif(self.gatetype == 'half'):
            for i in self.outputSocket[0].outgoing:
                i.incoming = None
                i.connected = False
            for i in self.outputSocket[1].outgoing:
                i.incoming = None
                i.connected = False
            for i in self.inputSockets:
                if(i.incoming!=None):
                    i.incoming.outgoing.remove(i)
            for i in lines: # to make lines white
                for j in i:
                    xo1 = self.outputSocket[0].rect.x
                    yo1 = self.outputSocket[0].rect.y
                    xo2 = self.outputSocket[1].rect.x
                    yo2 = self.outputSocket[1].rect.y
                    xi1 = self.inputSockets[0].rect.x
                    yi1 = self.inputSockets[0].rect.y
                    xi2 = self.inputSockets[1].rect.x
                    yi2 = self.inputSockets[1].rect.y
                    
                    xo1range = [xo1+i for i in range(-4,4,1)]
                    yo1range = [yo1+i for i in range(-4,4,1)]
                    xo2range = [xo2+i for i in range(-4,4,1)]
                    yo2range = [yo2+i for i in range(-4,4,1)]
                    xi1range = [xi1+i for i in range(-4,4,1)]
                    yi1range = [yi1+i for i in range(-4,4,1)]
                    xi2range = [xi2+i for i in range(-4,4,1)]
                    yi2range = [yi2+i for i in range(-4,4,1)]
                    
                    
                    if((j[0] in xo1range or j[1] in yo1range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xo2range or j[1] in yo2range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xi1range or j[1] in yi1range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    if((j[0] in xi2range or j[1] in yi2range) and (self == i[-1][0] or self==i[-1][1])):
                        i[-1].pop()
                        i[-1].append(orange)
                    
                    
        self.gateindex = None

        # remove the gate from the dictionary
        for i in gates_dict:
            if gates_dict.get(i) == self:
                self.gateindex = i
                del gates_dict[i]
                break

        for i in range(len(graph)):
            graph[i][self.gateindex] = 0 # remove dependencies for the gate from the graph

        for i in range(len(graph)):
            graph[self.gateindex][i] = 0 # set everything in the row of the gate in the graph to 0
                                

        if(isinstance(self.outputSocket, list)): # remove sprite from all groups
           for i in self.outputSocket:
               socket_list.remove(i)
               all_sprites.remove(i)
        else:
            socket_list.remove(self.outputSocket)
            all_sprites.remove(self.outputSocket)

        for i in self.inputSockets:
            socket_list.remove(i)
            all_sprites.remove(i)
                
        all_gates.remove(self)
        all_sprites.remove(self)

# ---------------------------------------------------------------------------------------------------------------------------------- #
        

class Socket(pygame.sprite.Sprite):
    def __init__(self, sock_type, bel_gate):
        global gates_dict
        pygame.sprite.Sprite.__init__(self)
        self.socket_type = sock_type
        self.val = None   # value of input or output is passed to gate through this
        self.belongs = None # to tell which gate this socket belongs to
        self.gatenumber = None
        for i in gates_dict:
            if gates_dict.get(i) == bel_gate:
                self.gatenumber = i
                break
        self.belongs = bel_gate   
        self.connected = False # check if there's already a connection to this socket. needed for inputs because you can't have multiple inputs
        self.outgoing = [] # to allow multiple output lines
        self.incoming = None # to check which socket it's connected from

        # draw the socket
        
        self.img = pygame.image.load('socket2.jpg')
        self.image = self.img.convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()

# ----------------------------------------------------------------------------------------------------------------------------------- #

        
# for the initial switch for user input  
class Switch(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.output = Socket('out',self)
        self.val = 0
        img = pygame.image.load('switch0.bmp')
        self.image = img.convert()
        self.image.set_colorkey(white)      
        self.rect = self.image.get_rect()
        self.set_output_values()
        self.gatetype = 'switch'

    def draw_socket(self): # no input sockets for switches
        self.output.rect.x = self.rect.x + 60
        self.output.rect.y = self.rect.y+17
        all_sprites.add(self.output)
        socket_list.add(self.output)
        
    def change_output(self): # set switch to on or off when clicked
        self.val = int(not self.val)
        if(self.val == 0):
            img = pygame.image.load('switch0.bmp')
        else:
            img = pygame.image.load('switch1.bmp')
        self.image = img.convert()
        self.image.set_colorkey(white)
        self.set_output_values()

    def delete(self): # delete the switch
        global all_sprites, socket_list, lines

        for i in self.output.outgoing:
            i.incoming = None
            i.connected = False
            
        for i in lines: # to make lines white
            for j in i:
                xo = self.output.rect.x
                yo = self.output.rect.y
                xorange = [xo+i for i in range(-4,4,1)]
                yorange = [yo+i for i in range(-4,4,1)]
                                
                if((j[0] in xorange or j[1] in yorange) and (self == i[-1][0] or self==i[-1][1])):
                    i[-1].pop()
                    i[-1].append(orange)
                
        socket_list.remove(self.output)
        all_sprites.remove(self.output)
        all_sprites.remove(self)

    def set_output_values(self): # transfer output value of switch to it's output socket
        self.output.val = self.val
        for i in self.output.outgoing:
            i.val = self.val

# ------------------------------------------------------------------------------------------------------------------------------- #



# Class to create buttons
class Button(pygame.sprite.Sprite):

    # Constructor. takes colour, width, height, text of button
    def __init__(self, img, otherimg,gatename):
        # Call parent class constructor
        pygame.sprite.Sprite.__init__(self)
        self.clicked = False #initially, all buttons created are not clicked.
        self.change = otherimg
        self.original = img
        # Create a button and fill it with a colour.
        self.image = img.convert()
        self.image.set_colorkey(white)
        # Fetch the rectangle with the dimensions of the image. Set position by using rect.x, rect.y
        # Coordinates to put the button at and accessing those coordinates knowing the size will also be easy.
        self.rect = self.image.get_rect()
        self.gatename=gatename

    # make button look like it's been selected
    def change_colour(self, flag): 
        x = self.rect.x
        y = self.rect.y
        global text
        global clickedgate
        if(flag == False):
            self.image = self.change.convert()
            clickedgate=self.gatename
            text = clickedgate.upper()+" selected."
            self.image.set_colorkey(white)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.image = self.original.convert()
            clickedgate = ""
            text = 'Select a gate'
            self.image.set_colorkey(white)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

# ------------------------------------------------------------------------------------------------------------------------------------------- #
    
            
# other methods:

# mouse click handler

def check_button(user):
    global pos1, points_list, socket_clicked, socket_selected, graph, button_clicked, socket1, socket2, socket_list, mouse_click_points, delete_set, all_gates, text, gates_dict
    hit = pygame.sprite.spritecollide(user, buttons_list, False)
    sock = pygame.sprite.spritecollide(user, socket_list, False)
    others = pygame.sprite.spritecollide(user, all_gates, False)
    
    
    if(len(hit)!=0): # checks if thing clicked on is a button
        if(clickedgate != "" and hit[0].gatename != clickedgate):
            text = 'Unselect previously selected button first' # checks if a button is already clicked
        elif(hit[0].gatename == 'submit'): # evaluates output
            final_output()
        else: # takes action for a button clicked when no other button is clicked
            hit[0].change_colour(hit[0].clicked)
            button_clicked = not(button_clicked)
            hit[0].clicked = not(hit[0].clicked)
            if(hit[0].gatename == 'delete'):
                delete_set = not(delete_set)
        
    elif(len(sock)!=0): # check if socket was clicked
        socket_clicked = not (socket_clicked)

        if(socket_clicked == True): # check if first socket was already clicked i.e. output socket
            socket1 = sock[0]
        if(socket1.socket_type == 'in' and socket_clicked == True):
            text = 'Invalid. You can connect only from output socket to input socket.'
            socket_clicked = False
        else: # add points for path
            text = 'Select upto 5 points on the path of connector or select socket to connect to directly'
            points_list.append(pygame.mouse.get_pos())
            
            if(socket_clicked == False): # check if input destination socket is  clicked
                socket2 = sock[0]
                # create connection between the two sockets
                if(socket2.connected!=True):
                    socket2.connected = True
                    socket1.outgoing.append(socket2) # add to socket's outgoing list
                    if(socket1.belongs.gatetype == 'switch'):
                        socket1.belongs.set_output_values()
                    socket2.incoming = socket1 # add to socket's incoming list
                    if(socket1.belongs.gatetype != 'switch'): # add dependency to graph
                        graph[socket1.gatenumber][socket2.gatenumber] = 1
                    points_list.append([socket1.belongs, socket2.belongs, black]) # add connection details to points_list
                    lines.append(points_list)
                    mouse_click_points = []
                    points_list = []
                    socket1 = None
                    socket2 = None

                else:
                    text = 'This input socket already has a connection' 
                                   
    elif(socket_clicked == True): # event handler for what happens if a destination socket is not picked within five points
        points_list.append(pygame.mouse.get_pos())
        mouse_click_points.append(pygame.mouse.get_pos()) 
        if(len(mouse_click_points)>5):
                text = 'Pick an output socket within five points'
                points_list = []
                mouse_click_points = []
                socket_clicked = False
        
    elif(button_clicked == True): # put gate on screen or delete as necessary
        pos1=pygame.mouse.get_pos()
        if(delete_set == True):
            if(len(others)!=0):
                others[0].delete()
        else:
            put_gate()

    elif(len(others)!=0): # handler for click on switch and for random clicks on existing gates
        if(others[0].gatetype == 'switch'):
            others[0].change_output()

# ...................................................................................................................................... #


def final_output(): # calculate final output
                global gates_dict, text
                digraph = []
                count  = 0
                flag = False

                # create digraph for sorting
                for i in range(len(graph)):
                        count = 0
                        digraph.append((i,[]))
                        for j in graph:
                            if(j[i]==1):
                                digraph[i][1].append(count)
                            count +=1

                # handle case when a gate(s) has been deleted
                keys = list(gates_dict.keys())

                i = 0
                while i<len(digraph):
                    if(digraph[i][0] not in keys):
                        digraph.remove(digraph[i])
                        i = 0
                    else:
                        i+=1
                    
                topo = []
                topo = topological_sort(digraph)

                if(len(topo)==0 and len(gates_dict)!=0):
                    digraph.append((0,[]))
                    topo = topological_sort(digraph)

                if(len(topo) == 0 and len(gates_dict)==0):
                    text = 'No gates connected'
                    return
                    
                output = 0
                for gate in topo:
                    gateObject = gates_dict[gate[0]]
                    Type = gateObject.gatetype
                    if(Type =='and'):
                        output = and_gate(gateObject.inputSockets[0].val,gateObject.inputSockets[1].val)
                        gateObject.set_output_values(output)
                    elif(Type =='not'):
                        output = not_gate(gateObject.inputSockets[0].val)
                        gateObject.set_output_values(output)
                    elif(Type == 'or'):
                        output = or_gate(gateObject.inputSockets[0].val,gateObject.inputSockets[1].val)
                        gateObject.set_output_values(output)
                    elif(Type == 'nand'):
                        output = nand_gate(gateObject.inputSockets[0].val,gateObject.inputSockets[1].val)
                        gateObject.set_output_values(output)
                    elif(Type =='nor'):
                        output = nor_gate(gateObject.inputSockets[0].val,gateObject.inputSockets[1].val)
                        gateObject.set_output_values(output)
                    elif(Type == 'xor'):
                        output = xor_gate(gateObject.inputSockets[0].val,gateObject.inputSockets[1].val)
                        gateObject.set_output_values(output)
                    elif(Type =='xnor'):
                        output = xnor_gate(gateObject.inputSockets[0].val,gateObject.inputSockets[1].val)
                        gateObject.set_output_values(output)
                    elif(Type =='HA'):
                        sum_1,carry = half_adder(gateObject.inputSockets[0].val,gateObject.inputSockets[1].val)
                        output = [carry, sum_1]
                        gateObject.set_output_values(output)
                    elif(Type =='FA'):
                        sum_1,carry = full_adder(gateObject.inputSockets[0].val,gateObject.inputSockets[1].val,gateObject.inputSockets[2].val)
                        output = [carry, sum_1]
                        gateObject.set_output_values(output)

                text = "The final output is : "+str(output)

# .................................................................................................................................................... #


def topological_sort(graph_unsorted):
    graph_sorted = []
    global text
    graph_unsorted = dict(graph_unsorted)

    # Run until the unsorted graph is empty.
    while graph_unsorted:
        acyclic = False
        for node, edges in list(graph_unsorted.items()):
            for edge in edges:
                if edge in graph_unsorted:
                    break
            else:
                acyclic = True
                del graph_unsorted[node]
                graph_sorted.append((node, edges))

        if not acyclic:
            text = 'Fatal error. Terminated.'

    return graph_sorted


# ................................................................................................................................................... #


def put_gate(): # put gate on canvas
             global gates_dict, gate_counter, graph, clickedgate, all_sprites, text
             if(clickedgate == 'switch'):
                 g = Switch()
             else:
                 g=Gates(clickedgate)
                 if(len(graph)==0):
                     graph.append([0])
                 else:
                     graph.append([0]*len(graph))

                 if(len(graph)!=1):
                     for i in range(len(graph)):
                         graph[i].append(0)
                         

             text = clickedgate.upper()+" selected. Click on a socket to connect."
             g.rect.x = pos1[0]
             g.rect.y = pos1[1]
             all_sprites.add(g)
             all_gates.add(g)
             g.draw_socket()
             l = all_gates.sprites()

# .................................................................................................................................................. #

             
def main():

    pygame.init()
    pygame.font.init()
    
    # create all buttons
    and_gate = Button(pygame.image.load("and.png"), pygame.image.load("and1.png"),"and")
    buttons_list.add(and_gate)
    all_sprites.add(and_gate)
    #set coordinates
    and_gate.rect.x = 50
    and_gate.rect.y = 20

    or_gate = Button(pygame.image.load("or.png"), pygame.image.load("or1.png"),"or")
    buttons_list.add(or_gate)
    all_sprites.add(or_gate)
    or_gate.rect.x = 50
    or_gate.rect.y = 80

    not_gate = Button(pygame.image.load("not.png"), pygame.image.load("not1.png"),"not")
    buttons_list.add(not_gate)
    all_sprites.add(not_gate)
    not_gate.rect.x = 50
    not_gate.rect.y = 140
   
    nand_gate = Button(pygame.image.load("nand.png"), pygame.image.load("nand1.png"),"nand")
    buttons_list.add(nand_gate)
    all_sprites.add(nand_gate)
    nand_gate.rect.x = 50
    nand_gate.rect.y = 200

    nor_gate = Button(pygame.image.load("nor.png"), pygame.image.load("nor1.png"),"nor")
    buttons_list.add(nor_gate)
    all_sprites.add(nor_gate)
    nor_gate.rect.x = 50
    nor_gate.rect.y = 260

    xor_gate = Button(pygame.image.load("xor.png"), pygame.image.load("xor1.png"),"xor")
    buttons_list.add(xor_gate)
    all_sprites.add(xor_gate)
    xor_gate.rect.x = 50
    xor_gate.rect.y = 320

    xnor_gate = Button(pygame.image.load("xnor.png"), pygame.image.load("xnor1.png"),"xnor")
    buttons_list.add(xnor_gate)
    all_sprites.add(xnor_gate)
    xnor_gate.rect.x = 50
    xnor_gate.rect.y = 380

    delete_gate = Button(pygame.image.load("delete.png"), pygame.image.load("delete.png"),"delete")
    buttons_list.add(delete_gate)
    all_sprites.add(delete_gate)
    delete_gate.rect.x = 1100
    delete_gate.rect.y = 610

    switch_gate = Button(pygame.image.load("switch0.bmp"), pygame.image.load("switch11.bmp"),"switch")
    buttons_list.add(switch_gate)
    all_sprites.add(switch_gate)
    switch_gate.rect.x = 70
    switch_gate.rect.y = 450

    save_gate = Button(pygame.image.load("save.png"), pygame.image.load("save.png"),"save")
    save_list.add(save_gate)
    all_sprites.add(save_gate)
    save_gate.rect.x = 1098
    save_gate.rect.y = 520

    submit = Button(pygame.image.load("submit.png"), pygame.image.load("submit.png"),"submit")
    buttons_list.add(submit)
    all_sprites.add(submit)
    submit.rect.x = 1098
    submit.rect.y = 430
    
    half = Button(pygame.image.load("ha.png"), pygame.image.load("ha1.png"),"HA")
    buttons_list.add(half)
    all_sprites.add(half)
    half.rect.x = 30
    half.rect.y = 510
    
    full = Button(pygame.image.load("fa.png"), pygame.image.load("fa1.png"),"FA")
    buttons_list.add(full)
    all_sprites.add(full)
    full.rect.x = 30
    full.rect.y = 600

    help_button = Button(pygame.image.load("help.png"), pygame.image.load("help.png"),"help")
    help_list.add(help_button)
    all_sprites.add(help_button)
    help_button.rect.x = 1160
    help_button.rect.y = 5
    

    
    # create user sprite
    user = Button(pygame.image.load("user.jpg"), pygame.image.load("user.jpg"),"user")
    all_sprites.add(user)
    close = False

    global myfont
    myfont = pygame.font.SysFont("Comic Sans MS",25)
    global label, text
    text = "Welcome to logic gate simulator. Select a gate."
    
    

    # main loop
    while close == False:
        if(delete_set):
            img = pygame.image.load("mouse.png")
        else:
            img = pygame.image.load('user.jpg')
        user.image = img.convert()
        user.image.set_colorkey(white)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
                pygame.quit()
            elif (event.type == pygame.MOUSEBUTTONDOWN):# and len(hit)==1):
                if(pygame.sprite.spritecollide(user, save_list, False)):
                            tktext.savefile()
                            b=tktext.a
                            b = b.strip()
                            b=b+".jpg"
                            pygame.image.save(screen,b) #str(b))
                            text = 'Image saved'
                elif(pygame.sprite.spritecollide(user, help_list, False)):
                            tktext.showfile()
                else:
                            check_button(user)
                
        screen.fill((255,200,100))
       
        pygame.draw.line(screen, (0,0,0), (200,0),(200,900))
      
        pos = pygame.mouse.get_pos()
        
        user.rect.x = pos[0]
        user.rect.y = pos[1]

        # update socket colours
        for i in socket_list:
            if(i.val == 0):
                i.img = pygame.image.load('socket1.jpg')
            elif(i.val == 1):
                i.img = pygame.image.load('socket.jpg')
            i.image = i.img.convert()
            i.image.set_colorkey(white)

       
        # draw non-sprite things
        all_sprites.draw(screen)
        for i in mouse_click_points:
            pygame.draw.circle(screen, red, i,3)
        for i in lines:
            pygame.draw.lines(screen, i[-1][2], False, i[0:(len(i)-1)])

        
        # draw the text of the status area
        label = myfont.render(text, 1, (0,0,0))
        screen.blit(label, (220,10))
        
        pygame.display.flip()

main()

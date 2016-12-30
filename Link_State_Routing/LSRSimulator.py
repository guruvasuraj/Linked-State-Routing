__author__ = 'GURU'


'''

Author : Natarajan, Guru Prasad
CWID: A20344932
Project - Link State Routing - Simulator


To execute the program, please follow the below steps:

1) Change the directory to the location where the program and the input files are available
2) Provide the command  'python LSRSimulator.py' to execute the program
'''



import os
import numpy

global topologyset
topologyset = False
global source
global destination
source = 0
destination = 0


# Function to validate user entered choices
'''
   Description: This function validates the choices entered by the user. If the user enters something other than a number,
   the program would show up an error message and display the main menu to the  user.
   This function also captures invalid choices for example if the user selects an option other than the one in the
   menu. It shows an error message.
'''

def validate_choices(choice):
    if not choice.isdigit():
        print "Please Enter a Number from the menu to proceed."
        return -1
    else:
        c = int(choice)
        if 6 < 1 < c:
            print "Please enter choices between 1 and 5."
            return -1
        else:
            return c


# Read the contents of the file and print the topology matrix
'''
   Description: This function reads the input file, which is in the form of  n x n  matrix.
               After reading the file it creates an n x n numpy array to be used by the other functions.
               From the topology matrix valid distances are set. Self-loops and unavailable connections are left out.
               In  order to review the original topology, the function prints each and every item in the numpy array.
'''
def review_topology(fname):
    global topology_matrix
    topology_matrix = []
    global topologyset
    topologyset = False
    global distances
    global nodes
    distances = {}
    nodes = []
    with open(fname) as f:
        for line in f:
            x = line.split()
            topology_matrix.append(x)
    topology_matrix = numpy.asarray(topology_matrix, dtype=int)
    topologyset = True
    # set the valid distances
    for i in range(len(topology_matrix)):
        temp = {}
        for j in range(len(topology_matrix)):
            if i != j:
                if topology_matrix[i][j] != -1:
                    temp[j + 1] = topology_matrix[i][j]
        distances[i + 1] = temp
        nodes.append(i + 1)
    #print the topology matrix
    print "\nReview original topology matrix:\n"
    for line in topology_matrix:
        for item in line:
            print int(item),
        print

#Function to modify the topology of the network
'''
    Description: This function gets the copy of the original topology matrix and removes the links between the node to be removed
    and every other nodes.
'''
def modifytopology(router,topology):
    global nodes
    rtr = int(router)
    topology=numpy.array(topology)
    distances.clear()
    nodes =[]
    for i in range(len(topology)):
        if i == rtr-1:
            for j in range(len(topology)):
                if i != j:
                    topology[i][j] = -1

    for i in range(len(topology)):
        for j in range(len(topology)):
             if j == rtr-1:
                if i != j:
                    topology[i][j] = -1
    for i in range(len(topology)):
        temp = {}
        for j in range(len(topology)):
            if i != j:
                if topology[i][j] != -1:
                    temp[j + 1] = topology[i][j]
        distances[i + 1] = temp
        nodes.append(i + 1)
    distances.pop(rtr) # remove the router from the distances dictionary
    for i in nodes:
        if i == rtr:
            nodes.remove(i) # remove the router

    #print the topology matrix -1
    print "\nReview original topology matrix:\n"
    for line in topology:
        for item in line:
            print int(item),
        print


#Algorithm to generate connection table for the given source
def dijkstra(source):
    global unseen
    global predecessors
    global seen
    global intermediate
    seen = {node: None for node in nodes}
    unseen = {node: None for node in nodes}
    predecessors = {node: None for node in nodes}
    intermediate = {node: None for node in nodes}
    currnode = int(source)
    currnodeDist = 0
    unseen[currnode] = currnodeDist

    while 1:
        for neighbor, distance in distances[currnode].iteritems():
            if neighbor in unseen:
                dist = currnodeDist + int(distance)
                if not unseen[neighbor] or dist < unseen[neighbor]: #condition to refine the path
                    unseen[neighbor] = dist
                    predecessors[neighbor] = currnode
                    if not intermediate[currnode]: # adding the intermediate nodes
                        intermediate[neighbor] = neighbor
                    else:
                        intermediate[neighbor] = intermediate[currnode]
        seen[currnode] = currnodeDist #mark the visited nodes
        del unseen[currnode] #delete visited nodes from the unvisited
        li = unseen.values()
        if not li: #repeat the process until the unseen dictionary is empty
            break;
        nodelist=[]
        for node in unseen.iteritems():
            if node[1]:
                nodelist.append(node)
        if nodelist:
            currnode, currnodeDist = sorted(nodelist, key=lambda tup: tup[1])[0] #sorts the items and picks the first tuple (i.e the one with the least distance)
# Function to generate the shortest path using the parent table generated by function dijkstra.


def shortest_path(source, destination):
    global route
    route = []
    src = int(source)
    dest = int(destination)
    route.append(dest)

    while dest != src:
        route.append(predecessors[dest]) #backtrack to get the optimal path between the source and the destination
        dest = predecessors[dest]
    route.reverse()


# Function to print the menu items
def printmenu():
    print "\n\t\t\t\t\t\t\t\t\t\t\t\t\tCS542 Link State Routing Simulator"
    print "\t\t\t\t\t\t\t\t\t\t\t\t------------------------------------------"
    print "(1) Create a Network Topology"
    print "(2) Build a Connection Table"
    print "(3) Shortest Path to Destination Router"
    print "(4) Print all connection tables"
    print "(5) Modify topology"
    print "(6) Exit"


choice = 0

while choice != 6: # Continue the loop until the user chooser option '5'

    printmenu() # Prints the menu items to the user
    choice = validate_choices(raw_input("\nMaster Command : "))

    if choice == 1:  # Input the file and create the topology matrix
        if topologyset:
            key = raw_input("\nNetwork Topology is already set. Press press [Enter] to redefine your choices")
        else:
            file = raw_input("\nInput original network topology matrix data file: ")
            if len(file) == 0:
                print "\nNo input file supplied. Please provide the input file."
            elif os.path.isfile(file):
                review_topology(file)
            else:
                print "\nInvalid file!!! Please input a valid file!!!."


    elif choice == 2:  # Build the connection table for the given source router

        if topologyset:
            source = raw_input("\nSelect a source router : ")
            if source == '':
                print "\n Source router not supplied. Please provide a source router to proceed"
            elif source.isdigit() and 0 < int(source) <= len(topology_matrix):
                if int(source) in distances:
                    dijkstra(source)
                else:
                    print "Router %s has been removed" %source
                print "\nRouter %s connection table" % source
                print "Destination\t\tInterface"
                for node in intermediate:
                    if intermediate[node] is None:
                        print "\t", node, "\t\t\t\t", "--"
                    else:
                        print "\t", node, "\t\t\t\t", intermediate[node]
            else:
                print "\nSource Router does not exist."

        else:
            print "\nNetwork topology matrix does not exist. Please create one by uploading a file to proceed."


    elif choice == 3:  # Get the shortest path with its cost for the given source destination pair

        if topologyset:

            destination = raw_input("\nSelect a destination router : ")
            if destination == '':
                print "\n Destination router not supplied. Please provide a destination router to proceed"
            elif destination.isdigit() and 0 < int(destination) <= len(topology_matrix):
                if int(source) == 0:
                    print "\n Source router not selected. Please select using option 2 to proceed."
                elif int(source) == int(destination):
                    print "\nSource and Destination routers cannot be the same. Please enter a different router "
                elif not predecessors[int(destination)]:
                    print "\nNo route exists between the given source %s and the Destination %s. \nPlease enter a different router to proceed." % (
                    source, destination)
                else:
                    shortest_path(source, destination)
                    print "\nThe shortest path from Router %s to Router %s : " % (source, destination),
                    for i in range(len(route)):
                        if i != len(route) - 1:
                            print str(route[i]) + str('->'),
                        else:
                            print str(route[i])
                    shortestdist = 0
                    if seen[int(destination)]:
                        shortestdist = seen[int(destination)]
                    print "\nThe total cost for reaching the destination : ", shortestdist

            else:
                print "\nDestination Router does not exist."

        else:
            print "\nNetwork topology matrix does not exist. Please create one by uploading a file to proceed."
    elif choice == 4: # Prints the connection table of all the nodes
        if topologyset:
            print "Connection table of all the nodes"
            for node in nodes:
                dijkstra(int(node))
                print "\nRouter %s connection table" % node
                print "Destination\t\tInterface"
                for node in intermediate:
                    if intermediate[node] is None:
                        print "\t",node, "\t\t\t\t", "--"
                    else:
                        print "\t",node, "\t\t\t\t", intermediate[node]

    elif choice == 5: # modifies the topology of the network
        if topologyset:
            flag = False
            router = raw_input("\nSelect a router to modify: ")
            if router == '':
                    print "\n Router not supplied. Please provide a router to proceed"
            elif router.isdigit() and 0 < int(router) <= len(topology_matrix):
                if int(source) == 0:
                    flag = False
                    source = raw_input("\nSource not provided. Please select a source:")
                    if int(source) == int(router):
                        flag = False
                        source = raw_input("\nSelected router set to modify. Please select another router:")
                if int(destination) == 0:
                    flag = False
                    destination = raw_input("\nDestination not provided. Please select a destination:")
                    if int(destination) == int(router):
                        flag = False
                        destination = raw_input("\nSelected router set to modify. Please select another router:")
                if int(router) == int(source):
                    flag = False
                    print "\nPlease select some other router to modify"
                elif int(router) == int(destination):
                    flag = False
                    print "\nSelected router is the destination. Please select some other router"
                else:
                    flag = True
                    modifytopology(router,topology_matrix.copy())
                    dijkstra(source)
                    print "\nRouter %s connection table" % source
                    print "Destination\t\tInterface"
                    for node in intermediate:
                        if intermediate[node] is None:
                            print "\t",node, "\t\t\t\t", "--"
                        else:
                            print "\t",node, "\t\t\t\t", intermediate[node]
                if flag:
                    if not predecessors[int(destination)]:
                        print "\nNo route exists between the given source %s and the Destination %s. \nPlease enter a different router to proceed." % (
                        source, destination)
                    else:
                        shortest_path(source, destination)
                        print "\nThe shortest path from Router %s to Router %s : " % (source, destination),
                        for i in range(len(route)):
                            if i != len(route) - 1:
                                print str(route[i]) + str('->'),
                            else:
                                print str(route[i])
                        shortestdist = 0
                        if seen[int(destination)]:
                            shortestdist = seen[int(destination)]
                        print "\nThe total cost is : ", shortestdist

        else:
            print "\nStart the program by supplying an input file"

    elif choice == 6: #Exits the program
        print "\n Exit CS542 project. Good Bye!"
        break

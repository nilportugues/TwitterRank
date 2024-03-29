import networkx as nx
import csv
import twint 
import numpy as np
import random

# construct a graph
userGraph = nx.DiGraph()

# read usernames from the .csv file
# store in a list
with open('test.csv') as data:
    reader = csv.reader(data)
    users_orig = [row[7] for row in reader] # get names from cols

# delete header
users_orig.pop(0) 

users = []
# pop out randomly  500 users from the user list

# rand = random.sample(range(0,1000), 3)
# for i in rand:
#     users.append(users_orig[i])
users.append(users_orig[905])

# add the users of the original tweets
userGraph.add_nodes_from(users)

# count the number of the network
count = 0 

# add the nodes and the edges of them into the graph
for user in users:
    c_follower = twint.Config()
    c_follower.Username = user
    c_follower.Store_object = True

    print()
    print("user: %s ; followers:" % (user))
    
    twint.run.Followers(c_follower)
    followers = twint.output.follows_list
    userGraph.add_nodes_from(followers)
    count += len(followers)

    print("count: %d" %(count))

    # clear the list 
    twint.output.follows_list = []

    for follower in followers:
        userGraph.add_edge(follower, user)

    print("count: %d" % (count))
        
    c_friends = twint.Config()
    c_friends.Username = user
    c_friends.Store_object = True

    print()
    print("user: %s ; friends:" % (user))

    twint.run.Following(c_friends)
    friends = twint.output.follows_list
    userGraph.add_nodes_from(friends)
    count += len(followers)

    print("count: %d" %(count))

    # clear the list 
    twint.output.follows_list = []

    for friend in friends:
        userGraph.add_edge(user, friend)

print("add Complete")

output = nx.to_numpy_array(userGraph)
np.save('test', output)
print("save complete")

# visualization

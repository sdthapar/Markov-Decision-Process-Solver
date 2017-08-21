import sys
import csv
import math
from decimal import *
from copy import copy

def main():

    print("Enter File Name")
    file_name = raw_input()
    print("Enter Gamma value")
    gamma = raw_input()
    gamma = Decimal(gamma)
    print("Enter Epsilon value")
    epsilon = raw_input()
    epsilon = Decimal(epsilon)
    input_file = file_name
    value_iteration = open('value_iteration.csv', "wb")
    policy_iteration = open('policy_iteration.csv', "wb")
    data = csv.reader(open(input_file), delimiter = ',')
    # writer = csv.writer(output_file, delimiter = )
    data.next()
    states = data.next()
    empty_count = states.count('')
    for i in range(0,empty_count):
        states.remove('')
    rewards = dict()
    data.next()
    for i in range(0, len(states)):
        r = data.next()
        rewards[r[0]] = Decimal(r[1])
        # print(r)

    # for key in rewards:
    #     print(key + "      "+ str(rewards[key]))
    data.next()
    actions = data.next()
    emp_count = actions.count('')
    for i in range(0,emp_count):
        actions.remove('')
    t = dict()
    for i in range(0,len(states)):
        t[states[i]] = dict()
        for j in range(0,len(actions)):
            t[states[i]][actions[j]] = []




    data.next()
    max_poss = len(states) * len(actions)
    for i in range(0,max_poss):
        trans = data.next()
        change = trans[2:]
        for j in range(0,len(change)):
            t[trans[0]][trans[1]].append(change[j])

    for i in range(0,len(states)):
        for j in range(0,len(actions)):
            print(t[states[i]][actions[j]])

    utilities = dict()
    utilities1 = dict()

    for i in range(0, len(states)):
        utilities[states[i]] = 0.0

    for i in range(0, len(states)):
        utilities1[states[i]] = 0.0

    for key in utilities:
        print(key+"     "+str(utilities[key]))
    #*************************** VALUE ITERATION ******************************
    #**************************************************************************
    #**************************************************************************
    #**************************************************************************

    delta = 0
    flag = True
    c = 0
    while flag == True:
        delta = 0
        utilities = copy(utilities1)
        for i in range(0,len(states)):
            sample = []
            # util_sum = 0
            k = states[i]
            # print(k)
            for v in t[k]:
                util_sum = 0
                lst = t[k][v]
                print(lst)
                for j in range(0,len(lst)):
                    if j+1<=len(lst):
                        if (j+1) % 2 == 0:
                            util_sum = util_sum + (Decimal(utilities[lst[j]])*Decimal(lst[j-1]))
                sample.append(util_sum)
            utilities1[states[i]] = Decimal(rewards[states[i]]) + (Decimal(gamma)*max(sample))
            if (Decimal(utilities1[states[i]])-Decimal(utilities[states[i]])) > Decimal(delta):
                print("U prime  = "+str(utilities1[states[i]]))
                print("U = "+str(Decimal(utilities[states[i]])))
                delta = abs(utilities1[states[i]]-Decimal(utilities[states[i]]))
        print("delta    = "+str(delta))
        print("product   = "+str((epsilon*(1-gamma))/gamma))
        if delta < (epsilon*(1-gamma))/gamma:
            flag = False
        else:
            flag = True
        c = c + 1
        print(c)

        value_policy = dict()
        directions_list = []
        for i in range(0,len(states)):
            sample = []
            # util_sum = 0
            k = states[i]
            # print(k)
            for v in t[k]:
                util_sum = 0
                lst = t[k][v]
                print(lst)
                for j in range(0,len(lst)):
                    if j+1<=len(lst):
                        if (j+1) % 2 == 0:
                            util_sum = util_sum + (Decimal(utilities[lst[j]])*Decimal(lst[j-1]))
                directions_list.append(v)
                sample.append(util_sum)
            index = sample.index(max(sample))
            optimal = directions_list[index]
            value_policy[states[i]] = optimal

        # for key in value_policy:
        #     print(key+"    "+value_policy[key])




    # for key in utilities1:
    #     print(key+"    "+str(utilities1[key]))

    value_iteration.write('file,'+input_file+'\n')
    value_iteration.write('gamma,'+str(gamma)+'\n')
    value_iteration.write('epsilon,'+str(epsilon)+'\n')
    value_iteration.write('iterations,'+str(c)+'\n')
    value_iteration.write('utilities\n')
    for i in range(0,len(states)):
        value_iteration.write(states[i]+','+str(utilities1[states[i]])+'\n')
    value_iteration.write('policy\n')
    for i in range(0,len(states)):
        value_iteration.write(states[i]+','+value_policy[states[i]]+'\n')




    #**************************************************************************
    #**************************************************************************
    #**************************************************************************



    #*************************** POLICY ITERATION *****************************
    #**************************************************************************
    #**************************************************************************
    #**************************************************************************
    default = 'North'
    policy = dict()
    policy1 = dict()
    policy_utility = dict() # Old dictionary of utilities for each corresponding state
    policy_utility1 = dict() # New dictionary of utilities for each corresponding state

    for i in range(0,len(states)):
        policy_utility[states[i]] = 0.0 # Setting initial utilities to 0.0

    def unchanged(x,y):
        # This method check whether the whether there is any difference in the values of the old policy dictionary and the new policy dictionary
        # If there is a difference we continue
        # Else we know that we converged to the right optimal policies since there is no more change and we break the loop
        f = True
        for i in range(0,len(states)):
            if x[states[i]] == y[states[i]]:
                f = True
            else:
                f = False
                break
        return f

    for i in range(0,len(states)):
        policy[states[i]] = default # Setting the initial value of old policy dictionary to the Default Direction = 'North'

    for i in range(0,len(states)): # Setting the initial value of new policy dictionary to the Default Direction = 'North'
        policy1[states[i]] = default
    for key in policy:
        print(key+"    "+policy[key])

    ctr = 0
    u_sum = 0
    b = True
    while b == True:
        policy = copy(policy1) # Setting the old policy dictionary equal to the updated new policy dictionary from the last iteration of the loop
        for i in range(0,len(states)):
            s = states[i]
            util_list = []
            direct_list = []
            # if ctr = 0:
            for v in t[s]:
                # v = policy[states[i]]
                u_sum = 0
                u_lst = t[s][v]
                for j in range(0,len(u_lst)):
                    if j+1<=len(u_lst):
                        if (j+1) % 2 == 0:
                            u_sum = u_sum + (Decimal(policy_utility[u_lst[j]])*Decimal(u_lst[j-1])) # Here I calculate the utility sum for each direction of a particular state
                direct_list.append(v) #
                util_list.append(u_sum)
            print(direct_list)
            print(util_list)
            if ctr == 0:
                # In the first iteration when  ctr = 0 I just follow the default policy
                policy_utility[states[i]] = rewards[states[i]] + (Decimal(gamma)*sample[direct_list.index(policy[states[i]])])
            else:
                # In iterations after the first iteration I find the maximum utility direction
                print("MAX ============ "+ str(max(util_list)))
                print("Previous utility   =  "+str(policy_utility[states[i]]))
                u = rewards[states[i]] + (Decimal(gamma)*max(util_list)) # MAXIMUM utility for the state we are considering
                print("New max utility  =  "+str(u))
                print("NEW --------- "+states[i]+" "+direct_list[util_list.index(max(util_list))])
                # policy_utility[states[i]] = rewards[states[i]] + (Decimal(gamma)*max(util_list))
                # policy1[states[i]] = direct_list[util_list.index(max(util_list))]

                # policy1[states[i]] = direct_list[util_list.index(max(util_list))]
                if u > policy_utility[states[i]]:
                    # Here I check whether the new max utility is better than the previous utility
                    # I update the policy to the new policy and the utility to the maximum utility for this particular state
                    print(" update update update update update update update update update ")
                    policy_utility[states[i]] = rewards[states[i]] + (Decimal(gamma)*max(util_list))
                    policy1[states[i]] = direct_list[util_list.index(max(util_list))]
                else:
                    # policy_utility[states[i]] = rewards[states[i]] + (Decimal(gamma)*max(util_list))
                    # if the maximum utility is not better than the previous utility then I just stick to my old policy
                    # do not update the utility in the policy_utility dictionary
                    policy1[states[i]] = policy[states[i]]



        for key in policy:
            print("OLD "+key+"   "+policy[key])

        for key in policy1:
            print("NEW "+key+"   "+policy[key])

        for key in policy_utility:
            print(key+"     "+str(policy_utility[key]))



        ctr = ctr + 1 # I increase the counter after every iteration
        print(ctr)
        if ctr > 1:
            if unchanged(policy1, policy):
                # if unchanged return true then we break the loop and stop
                # Since we have converged to the optimal policy
                b = False
            else:
                b = True


    policy_iteration.write('file,'+input_file+'\n')
    policy_iteration.write('gamma,'+str(gamma)+'\n')
    policy_iteration.write('iterations,'+str(ctr)+'\n')
    policy_iteration.write('utilities\n')
    for i in range(0,len(states)):
        policy_iteration.write(states[i]+','+str(policy_utility[states[i]])+'\n')
    policy_iteration.write('policy\n')
    for i in range(0,len(states)):
        policy_iteration.write(states[i]+','+policy1[states[i]]+'\n')





















if __name__ == "__main__":
    main()

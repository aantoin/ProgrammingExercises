

def findMinimumRoutes(airports,routes,starting_port):
    '''Finds the minimum number of routes so that the starting airport can reach all other airports'''
    if starting_port not in airports:
        return []

    airport_ids = {airports[i]:i for i in range(len(airports))}
    airport_route_lists = {airport:set() for airport in airports}
    for route in routes:
        airport_route_lists[route[0]].add(route[1])

    ignored_airports = [x==starting_port for x in airports]
    airports_to_search = set([starting_port])
    while len(airports_to_search)>0:
        airport_to_search = airports_to_search.pop()
        for destination in airport_route_lists[airport_to_search]:
            if not ignored_airports[airport_ids[destination]]:
                ignored_airports[airport_ids[destination]]=True
                airports_to_search.add(destination)
        if airport_to_search in airports_to_search:
            airports_to_search.remove(airport_to_search)


    airport_groups = {airport:None for airport in airports}
    for id in range(len(airports)):
        if not ignored_airports[id]:
            base_airport = airports[id]
            if airport_groups[base_airport] is None:
                airports_to_search = set([base_airport])
                airport_groups[base_airport]=base_airport
                while len(airports_to_search)>0:
                    airport_to_search = airports_to_search.pop()
                    for destination in airport_route_lists[airport_to_search]:
                        if not ignored_airports[airport_ids[destination]] and airport_groups[destination]!=base_airport:
                            airports_to_search.add(destination)
                            airport_groups[destination]=base_airport


    new_routes = [(starting_port,x) for x in set(y for y in airport_groups.values() if y is not None)]
    return new_routes


def testCompleteness(airports,routes,starting_port):
    '''Test that the starting airport can reach all airports given a list of routes'''
    if starting_port not in airports:
        return True
    found = set([starting_port])
    airports_to_search = set([starting_port])
    while len(airports_to_search)>0:
        airport_to_search = airports_to_search.pop()
        for route in routes:
            if route[0]==airport_to_search and route[1] not in found:
                found.add(route[1])
                airports_to_search.add(route[1])
    return found == set(airports)

def genRouteCombos(routes,n):
    if n==0:
        yield []
    elif n==1:
        for route in routes:
            yield [route]
    else:
        for route_list in genRouteCombos(routes,n-1):
            for route in routes:
                if route not in route_list:
                    yield route_list+[route]


def testMinimum(airports,routes,new_routes,starting_port):
    '''Brute force test all combinations of additional routes to find the minimum (to check the answer from findMinimumRoutes())'''
    import itertools

    if len(new_routes)==0:
        return testCompleteness(airports,routes,starting_port)

    route_combinations = [(x,y) for x in airports for y in airports if x!=y and (x,y) not in routes]
    #total_combinations = [[x] for x in route_combinations]
    print(f"Checking solution is minimum at depth (max {len(new_routes)-1}): ",end='')
    i=0
    while i<len(new_routes):
        print(('' if i==0 else ',')+str(i),end=('' if i<len(new_routes)-1 else '\n'),flush=True)
        #Brute force check all solutions with i routes
        for x in genRouteCombos(route_combinations,i):
            if testCompleteness(airports,routes+x,starting_port):
                print("\nBetter Result: ",x,"Old Result: ",new_routes)
                return False
        i+=1
    return True


def generateTestData(min_airports=0,max_airports=7,min_routes=0,max_routes=-1):
    '''Generate test data for findMinimumRoutes()'''
    import random

    max_airports = max(max_airports,0)
    min_airports = min(max(min_airports,0),max_airports)
    num_airports = random.randrange(min_airports,max_airports+1)
    airports = [chr(ord('A')+i)*3 for i in range(num_airports)]

    if max_routes<0 or max_routes>num_airports**2:
        max_routes = num_airports**2
    min_routes = min(max(min_routes,0),max_routes)
    num_routes = random.randrange(min_routes,max_routes+1)
    routes = random.sample([(x,y) for x in airports for y in airports],num_routes)

    starting_port = '' if num_airports==0 else random.sample(airports,1)[0]

    return (airports,routes,starting_port)

if __name__ == "__main__":
    '''Create a bunch of test cases for findMinimumRoutes()'''
    failure = False
    for max_airports in range(8):
        for i in range(1000):
            print("###",f"max_airports: {max_airports}",i,"###")
            airports,routes,starting_port = generateTestData(max_airports=max_airports)
            #print("ARS",(airports,routes,starting_port))

            new_routes = findMinimumRoutes(airports,routes,starting_port)
            #print("New Routes",new_routes)

            TC=testCompleteness(airports,routes+new_routes,starting_port)
            #print("Test Complete",TC)

            TM=testMinimum(airports,routes,new_routes,starting_port)
            #print("Test Minimum ",TM)

            if not TC or not TM:
                failure=True
                print("failed with",(airports,routes,starting_port))
                break
        else:
            print(f"Success with {max_airports}!")
        if failure:
            break


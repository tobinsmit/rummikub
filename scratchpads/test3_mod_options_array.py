import time

def inc_or_double_to_100(x, verbose=False):
    ''' Finds one of the shortest routes from x to 100 '''

    # starting_route = [x]
    all_routes = [[x]]

    def vprint(*args):
        ''' If verbose, prints args '''
        if verbose:
            print(*args)

    def vprint_all_routes(all_routes):
        ''' If verbose, prints all_routes with nice formatting '''
        if verbose:
            print('\tall_routes = [')
            for this_route in all_routes:
                print('\t\t',this_route)
            print('\t]')

    for this_route in all_routes:
        vprint('this_route =', this_route)
        x = this_route[-1]
        options = [2*x, x+1]
        for option in options:
            new_route = [*this_route, option]
            vprint('\tnew_route =', new_route)
            if option == 100:
                vprint('EUREKA! route =', new_route)
                return new_route
            elif option < 100:
                all_routes.append(new_route)
        vprint_all_routes(all_routes)



result = inc_or_double_to_100(12, verbose=True)

# Measure time for 100 calls with x=13
print('\nDoing 100 calls')
start = time.time()
for i in range(100):
    result = inc_or_double_to_100(13)
end = time.time()
total_time = end - start
print(f'Took {total_time:0.3f}s for 100 calls with x=13')

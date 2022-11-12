
def inc_or_double_to_100(routes):
    for route in routes:
        # print('\troute', route)
        x = route[-1]
        options = [2*x, x+1]
        for option in options:
            new_route = [*route, option]
            if option == 100:
                return new_route
            elif option < 100:
                routes.append(new_route)



if __name__ == '__main__':
    import time
    print(inc_or_double_to_100([[26]]))
    start = time.time()
    for i in range(100):
        inc_or_double_to_100([[26]])
    end = time.time()
    print(f'Took {end-start}sec')

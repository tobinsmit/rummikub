
def inc_or_double_to_100(routes):
    new_routes = []
    for route in routes:
        x = route[-1]

        x_double = 2*x
        if x_double == 100:
            return [*route, x_double]

        x_inc = x + 1
        if x_inc == 100:
            return [*route, x_inc]

        new_routes.append([*route, x_double])
        new_routes.append([*route, x_inc])

    return inc_or_double_to_100(new_routes)



if __name__ == '__main__':
    import time
    start = time.time()
    print(inc_or_double_to_100([[26]]))
    end = time.time()
    print(f'Took {end-start}sec')

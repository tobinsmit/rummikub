
def inc_or_double_to_100(routes):
    for route in routes:
        # print('\troute', route)
        x = route[-1]

        x_double = 2*x
        if x_double == 100:
            return [*route, x_double]
        elif x_double < 100:
            routes.append([*route, x_double])

        x_inc = x + 1
        if x_inc == 100:
            return [*route, x_inc]
        elif x_inc < 100:
            routes.append([*route, x_inc])



if __name__ == '__main__':
    import time
    print(inc_or_double_to_100([[26]]))
    start = time.time()
    for i in range(100):
        inc_or_double_to_100([[26]])
    end = time.time()
    print(f'Took {end-start}sec')

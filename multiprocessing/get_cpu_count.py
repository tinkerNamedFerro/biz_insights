# Parallelizing using Pool.apply()

import multiprocessing as mp


def main():

    # Step 1: Init multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())

    # Step 2: `pool.apply` the `howmany_within_range()`
    results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]

    # Step 3: Don't forget to close
    pool.close()    

    print(results[:10])
    #> [3, 1, 4, 4, 4, 2, 1, 1, 3, 3]

if __name__ == '__main__':
    main()
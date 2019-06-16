import datetime
import multiprocessing
import hashlib
import sys
from string import ascii_lowercase
import random
import string

def randomString(stringLength=5):
    lis = list(ascii_lowercase)
    return ''.join(random.choice(string.ascii_lowercase) for i in range(stringLength))


def computesha(process_number, number_of_processes, max_counter, randoms, results):

    counter = process_number
    data = 'AbeVGjkdgjkLPZOoIZEIELfVmSQKKWVofgJwnmsdKVDXbibzZEnFsrWWjRbOZaNnqkxechmwrb'
    data2 = 'kiG9w3' 
    #random_string = randoms
    while counter < max_counter: 
        hash = data + str(counter) + data2 #append random string or the counter
        newHash = hashlib.sha1(hash.encode()).hexdigest()        
        if newHash[:5] == '00000':
            print(str(newHash))
            print(str(randoms))
            print("Found one!!!   " + str(datetime.datetime.now()))
            results.put((str(newHash), str(counter)))
            break     
        counter += number_of_processes 
        #random_string = randomString()

if __name__ == '__main__':

    d1 = datetime.datetime.now()
    print("Start timestamp" + str(d1))

   
    number_of_processes = int(8)
    max_counter = int(sys.maxsize ** 100)
    randoms = randomString() 
    results = multiprocessing.Queue()

    processes = []
 
    for i in range(number_of_processes):
        p = multiprocessing.Process(target=computesha, args=(i,
                                                             number_of_processes,
                                                             max_counter, 
                                                             randoms, 
                                                             results))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
        if not results.empty():
             p.terminate()
             #break

    for p in processes:
         p.terminate()


    while not results.empty():
        print(results.get())
    results.close()

    d2 = datetime.datetime.now() 
    print("End timestamp " + str(d2))
    print("Elapsed time: " + str((d2-d1))) 
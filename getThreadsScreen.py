#!/usr/bin/python3

import sys, getopt, os, time 


#method = "gnomeTabs"
method = "screen"
pythonVersion = "python3"

outputFile = "ff23_1631270380000000.txt"

def echoCommand(message):
    return "echo '" + message + "';"

def main(argv):
    startPage = 0
    endPage = 0
    parallelCount = 0
    try:
        opts, args = getopt.getopt(argv,'s:e:p:')
    except getopt.GetoptError:
        print ('startBrainWallet.py -s <startPage> -e <endPage> -p <parallelCount>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('startBrainWallet.py -s <startPage> -e <endPage> -p <parallelCount>')
            sys.exit()
        elif opt in ("-s", "--start"):
            startPage = int(arg)
        elif opt in ("-e", "--end"):
            endPage = int(arg)
        elif opt in ("-p", "--parallelCount"):
            parallelCount = int(arg)   

    #-----------------------------------------------------------------
    print ('start unix time ', startPage)
    print ('end unix time ', endPage)
    print ('end of simultaneous instances\n', parallelCount)

    timeDelta = (endPage - startPage)/ parallelCount
    count = 0

    # run with bloom file selected
    for instance in range(0,int(parallelCount)):
        instanceStartPage = str(round(startPage+(instance*timeDelta)))
        instanceEndPage = str(round(startPage+((instance+1) *timeDelta)))

        getThreadsCommand = f'{pythonVersion} ./getThreads.py -s {instanceStartPage} -e {instanceEndPage} -p 0' 

        # print(instanceStartPage + " " + instanceEndPage) 
        if method == "gnomeTabs":
            os.system('gnome-terminal --tab --active -- bash -c "' + 
                echoCommand(f'{instanceStartPage}-{instanceEndPage}') + 
                echoCommand(getThreadsCommand)+
                getThreadsCommand +
            'exec bash"')
        else:
            command = f'screen -S getThreads-{instanceStartPage}-{instanceEndPage} -dm bash -c "' + echoCommand(f'{instanceStartPage}-{instanceEndPage}') + echoCommand(getThreadsCommand) + getThreadsCommand + ' exec sh"'
            print(f'{instanceStartPage}-{instanceEndPage} starting')
            time.sleep(1)
            count += 1
            os.system(command)

if __name__ == "__main__":
    main(sys.argv[1:])

    

#!/usr/bin/python3
#coding=utf-8
#Python3
#By Rick Wu 20200927

import subprocess
import json
import re


def ParseLog (whoami, filename):
    skip, pas, fail, duration = 0, 0, 0, 0
    print('Start parse JSON for ' + filename + ' .....')
    with open('/home/' + whoami + '/tmp/submission.json') as file:
        data = json.load(file)
    for key in data['results']:
        if key['status'] == 'skip':
            skip+=1
        elif key['status'] == 'pass':
            pas+=1
        else:
            fail+=1
        duration = duration + key['duration']
    with open('/home/'+ whoami + '/' + filename + '.report','a') as LogFile:
        print("Version tested: "+data['distribution']['description'], file = LogFile)
        print('Number of tests run: ' + str(skip+pas+fail), file = LogFile)
        print('Outcome:', file = LogFile)
        print(' -skip: ' + str(skip) + ' (' + str(int(round(skip/(skip+pas+fail),2)*100)) + '%)', file = LogFile)
        print(' -fail: ' + str(fail) + ' (' + str(int(round(fail/(skip+pas+fail),2)*100)) + '%)', file = LogFile)
        print(' -pass: ' + str(pas) + ' (' + str(int(round(pas/(skip+pas+fail),2)*100)) + '%)', file = LogFile)
        print('Total run duration: ' + str(int(round(duration,0))) + ' seconds', file = LogFile)
    print('Parse log done...\n''Please check '+ filename + '.report for detail.')


def UnzipSub (filepath, filename):
    print('Unzipping ' + filename + '.....')
    subprocess.run('mkdir ~/tmp', shell=True)
    subprocess.run('tar -C ~/tmp -xvJf ' + filepath + '/' + filename, shell=True,)
    print('Unzip Done .....')


def ClearSub ():
    subprocess.run('rm -rf ~/tmp', shell=True)





if __name__ == "__main__":
    FilePath = input("Please input your submissions file path. e.g. /home/username/.local/share/checkbox-ng/ :")
    if FilePath == "":
        WhoAmI = subprocess.run('whoami', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        FilePath = '/home/' + WhoAmI + '/.local/share/checkbox-ng/'
    SubStr = subprocess.run('ls ' + FilePath + '*.xz', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip() #find all submission log file
    if SubStr == "":
        print('Did not find Submission files!')    
    elif len(re.findall('submission',SubStr)) == 0 :
        print('Did not find Submission files!')
    else:
        SubList = re.findall(r'(?:[\w\s.-]+[a-z]+\_\d+\-\d+\-\w+(?:\.\w+)+)',SubStr) #find submisson file name from path and turn into a list
        SubDict = {x+1:SubList[x] for x in range(len(SubList))} #turn submission file name list into dict
        print('================== Submission List ===================')
        for key in SubDict.keys():
            print(str(key) + ' : ' + SubDict[key])
        print('Any other key for all of above')
        SelectSub = input('Select one to parse log: ')
        if SelectSub in SubDict.keys():
            UnzipSub(FilePath, SubDict[int(SelectSub)])
            ParseLog(WhoAmI, SubDict[int(SelectSub)])
            ClearSub()
        else:
            for key in SubDict.keys():
                UnzipSub(FilePath, SubDict[key])
                ParseLog(WhoAmI, SubDict[key])
                ClearSub()

#coding=utf-8
#Python3
#By Rick Wu 20200927

import subprocess
import json
import re


def ParseLog (filepath, filename):
    print('Start parse JSON for ' + filename + ' .....')
    #with open('/home/rick/.local/share/checkbox-ng/submission.json') as file:
    with open(filepath+'submission.json') as file:
        data = json.load(file)
    LogFile = open(filename+'.report','a')
    print("Version tested: "+data['distribution']['description'], file = LogFile)
    skip = sum(key['status'] == 'skip' for key in data['results'])
    pas = sum(key['status'] == 'pass' for key in data['results'])
    fail = sum(key['status'] == 'fail' for key in data['results'])
    duration = sum(key['duration'] for key in data['results'])
    print('Number of tests run: ' + str(skip+pas+fail), file = LogFile)
    print('Outcome:', file = LogFile)
    print(' -skip: ' + str(skip) + ' (' + str(int(round(skip/(skip+pas+fail),2)*100)) + '%)', file = LogFile)
    print(' -fail: ' + str(fail) + ' (' + str(int(round(fail/(skip+pas+fail),2)*100)) + '%)', file = LogFile)
    print(' -pass: ' + str(pas) + ' (' + str(int(round(pas/(skip+pas+fail),2)*100)) + '%)', file = LogFile)
    print('Total run duration: ' + str(int(round(duration,0))) + ' seconds', file = LogFile)
    LogFile.close()
    print('Parse log done...\n''Please check \"'+ filename + '.report\" for detail.')

def UnzipSub (filepath, filename):
    print('Unzipping ' + filename + '.....')
    subprocess.run('tar -xvJf ' + filepath + '/' + filename, shell=True,)
    print('Unzip Done .....')
def ClearSub (filepath):
    subprocess.run('rm ' + filepath + 'submission.json', shell=True)
    subprocess.run('rm ' + filepath + 'submission.junit', shell=True)
    subprocess.run('rm ' + filepath + 'submission.xlsx', shell=True)
    subprocess.run('rm ' + filepath + 'submission.html', shell=True)
    subprocess.run('rm -rf ' + filepath + 'test_output', shell=True)
    subprocess.run('rm -rf ' + filepath + 'attachment_files', shell=True)



WhoAmI = subprocess.run('whoami', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
FilePath = '/home/' + WhoAmI + '/.local/share/checkbox-ng/'
SubStr = subprocess.run('ls ' + FilePath + '*.xz', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip() #find all submission log file
if len(re.findall("No such file",SubStr)) != 0 :
    print('Did not find Submission folder!')
else:
    SubList = re.findall(r'(?:[\w\s.-]+[a-z]+\_\d+\-\d+\-\w+(?:\.\w+)+)',SubStr) #find submisson file name from path and turn into a list
    SubDict = {x+1:SubList[x] for x in range(len(SubList))} #turn submission file name list into dict
    print('================== Submission List ===================')
    for key in SubDict.keys():
        print(str(key) + ' : ' + SubDict[key])
    print('Any other key for all of above')
    SelectSub = input('Select one to parse log: ')
    if SelectSub.isdigit() != True:
        for key in SubDict.keys():
            UnzipSub(FilePath, SubDict[key])
            ParseLog(FilePath, SubDict[key])
            ClearSub(FilePath)
    elif int(SelectSub) in SubDict.keys():
        UnzipSub(FilePath, SubDict[int(SelectSub)])
        ParseLog(FilePath, SubDict[int(SelectSub)])
        ClearSub(FilePath)
    else:
        for key in SubDict.keys():
            UnzipSub(FilePath, SubDict[key])
            ParseLog(FilePath, SubDict[key])
            ClearSub(FilePath)



#filename = filepath.split('/')[-1].split('.tar')[0]


'''
for cnt in range(len(data['results'])):
    if data['results'][cnt]['status'] == "skip":
    print(data['results'][cnt]['status'])
'''
    

def hi():
    f = open('/textsForCrons/text1.txt', 'a')
    print('printed from crontab', file=f)
    f.close()

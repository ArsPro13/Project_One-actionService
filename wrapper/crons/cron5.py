def hi():
    f = open('/textsForCrons/text5.txt', 'a')
    print('printed from crontab', file=f)
    f.close()

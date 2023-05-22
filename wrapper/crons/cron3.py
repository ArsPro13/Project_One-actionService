def hi():
    f = open('/textsForCrons/text3.txt', 'a')
    print('printed from crontab', file=f)
    f.close()

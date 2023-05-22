def hi():
    f = open('/textsForCrons/text4.txt', 'a')
    print('printed from crontab', file=f)
    f.close()

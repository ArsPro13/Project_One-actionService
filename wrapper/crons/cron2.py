def hi():
    f = open('/textsForCrons/text2.txt', 'a')
    print('printed from crontab', file=f)
    f.close()

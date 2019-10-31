import time ,threading 
from random import choice


class wtf:
    def __init__(self):
        self.alldown = list(range(40))
        self.balance = list()


    def deldel(self):
        while len(self.balance) > 0:
            print("del",self.balance.pop())
            time.sleep(0.5)

    def download(self):
        while len(self.alldown) > 0:
            if len(self.balance) < 20:
                tmp = self.alldown.pop()
                print('download',tmp)        
                time.sleep(0.1)
            time.sleep(0.1)
        self.flag = True

    def process(self):
        t1 = threading.Thread(target = self.download)
        t2 = threading.Thread(target = self.deldel )#,args = (8,))
        #t3 = threading.Thread(target = self.deldel )#,args = (8,))
        t2.start()
        t1.start()
        #t3.start()
        t1.join()
        t2.join()
        #t3.join()
        print (self.balance)
        print (self.alldown)

if __name__ == '__main__':
    w = wtf()
    w.process()

        

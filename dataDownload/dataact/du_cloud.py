import time ,threading 

class wtf:
    def __init__(self):
        self.alldown = list(range(40))
        self.balance = list()

    def deldel(self):
        while len(self.balance) > 0:
            print("del",self.balance.pop())
            time.sleep(1)

    def download(self):
        while len(self.alldown) > 0:
            if len(self.balance) < 20:
                tmp = self.alldown.pop()
                print('download',tmp)        
                self.balance.append(tmp)
                time.sleep(0.1)
            time.sleep(0.1)

    def process(self):
        t1 = threading.Thread(target = self.download)
        t2 = threading.Thread(target = self.deldel )#,args = (8,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print (self.balance)
        print (self.alldown)

if __name__ == '__main__':
    w = wtf()
    w.process()#https://www.cnblogs.com/andylhc/p/9686954.html

        
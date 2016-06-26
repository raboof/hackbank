import time
class log:
    def __init__(self,SID,master):
        self.SID=SID
        self.master=master
    
    def startup(self):
        self.master.send_message(False,'log',"Log has startup")

    def log(self,action,text):
        with open("data/revbank.log","a") as logfile:
          logfile.write(time.strftime("%Y-%m-%d_%H:%M:%S")+' '+action+' '+text+'\n')
          logfile.close()
        self.master.send_message(False,'log',action+" >> "+text)

    def hook_balance(self,(usr,had,has,trxID)):
        if had>has:
            self.log("BALANCE","%-10d %s had %+.02f, lost %+.02f, now has %+.02f" % ( trxID,usr,had,0-(had-has),has))
        else:
            self.log("BALANCE","%-10d %s had %+.02f, gained %+.02f, now has %+.02f" % ( trxID,usr,had,has-had,has ))

    def hook_post_checkout(self,text):
        for rr in self.master.receipt.receipt:
          if rr['Lose']:
             gol="LOSE"
          else:
             gol="GAIN"
          self.log("CHECKOUT","%-10d %s %d * %10.2f %s EUR %10.2f # %s" % ( self.master.transID,rr['beni'],rr['count'],rr['value'],gol,rr['count']*rr['value'],rr['description']) )

    def input(self,text):
        pass

    def pre_input(self,text):
        self.log("PROMPT",self.master.prompt+" >> "+text)
        #self.master.send_message(False,'log',self.master.prompt+" >> "+text)
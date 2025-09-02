import multiprocessing
import time
import random

class Message:
    def __init__(self, request_id: int, timestamp: int, tip: str):
        self.request_id = request_id  # ID zahtjeva
        self.timestamp = timestamp    # Logički sat
        self.tip = tip                # Tip poruke: "ZAH", "ODG", "IZL"
    
    def __str__(self):
        return f"{self.tip}({self.request_id}, {self.timestamp})"



class Philosopher(multiprocessing.Process):
    def __init__(self, id, message_queues):
        super().__init__()
        self.id = id
        self.local_time = random.randint(1, 500)
        self.left = True
        self.right = False
        self.message_queues = message_queues
        self.lmessages = []
        self.rmessages = []
        self.lzah = False
        self.rzah = False
        self.lindex = (id - 1) % 5
        self.rindex = (id + 1) % 5

    def run(self):
        print(f"Filozof {self.id} ima vrijednost logičkog sata {self.local_time}.")
        while True:
            print(f"Filozof {self.id} misli...")
            time.sleep(random.uniform(6, 14))  # Simuliramo vrijeme razmišljanja

            if(self.lzah == False):
                mess = Message(self.id, self.local_time, "ZAH")
                print(f"Filozof {self.id} šalje poruku filozofu {self.lindex}: {mess}")
                self.lmessages.append(mess)
                self.message_queues[self.lindex].put(mess)
                self.lzah = True

            if(self.rzah == False):
                mess = Message(self.id, self.local_time, "ZAH")
                print(f"Filozof {self.id} šalje poruku filozofu {self.rindex}: {mess}")
                self.rmessages.append(mess)
                self.message_queues[self.rindex].put(mess)
                self.rzah = True
            
            msg = self.message_queues[self.id].get()
            if((msg.request_id + 1) % 5 == self.id):
                print(f"Filozof {self.id} prima poruku: {msg}")
                if(msg.tip == "ZAH"):
                    self.lmessages.append(msg)
                    self.local_time = max(self.local_time,msg.timestamp) + 1
                    newmes = Message(self.id,self.local_time, "ODG")
                    self.message_queues[msg.request_id].put(newmes)
                if(msg.tip == "ODG" and len(self.lmessages) >= 2):
                    if(self.lmessages[0].timestamp < self.lmessages[1].timestamp):
                        self.left = True
                    elif(self.lmessages[0].timestamp == self.lmessages[1].timestamp):
                        if(self.id > msg.request_id):
                            self.left = True
                        else:
                            self.left = False
                    else:
                        self.left = False
                if(msg.tip == "IZL"):
                    if(msg.request_id == self.lindex):
                        self.left = True
                    if(msg.request_id == self.rindex):
                        self.right = True

            if((msg.request_id - 1) % 5 == self.id):
                print(f"Filozof {self.id} prima poruku: {msg}")
                if(msg.tip == "ZAH"):
                    self.rmessages.append(msg)
                    self.local_time = max(self.local_time,msg.timestamp) + 1
                    newmes = Message(self.id,self.local_time, "ODG")
                    self.message_queues[msg.request_id].put(newmes)
                if(msg.tip == "ODG" and  len(self.rmessages) >= 2):
                    if(self.rmessages[0].timestamp < self.rmessages[1].timestamp):
                        self.right = True
                    elif(self.rmessages[0] == self.rmessages[1]):
                        if(self.id > msg.request_id):
                            self.right = True
                        else:
                            self.right = False
                    else:
                        self.right = False
                if(msg.tip == "IZL"):
                    if(msg.request_id == self.lindex):
                        self.left = True
                    if(msg.request_id == self.rindex):
                        self.right = True
                

            
            if(self.left == True and self.right == True):
                print(f"Filozof {self.id} jede...")
                time.sleep(random.uniform(6, 14))  # Simuliramo vrijeme jedenja
                self.left = False
                self.right = False
                self.lmessages.clear()  # Briše sve elemente iz lmessages
                self.rmessages.clear()  # Briše sve elemente iz rmessages
                newmes = Message(self.id,self.local_time, "IZL")
                print(f"Filozof {self.id} oslobađa štapiće.")
                self.message_queues[self.lindex].put(newmes)
                self.message_queues[self.rindex].put(newmes)
                self.lzah = False
                self.rzah = False



def main():
    num_philosophers = 5
    message_queues = [multiprocessing.Queue() for _ in range(num_philosophers)]
    philosophers = []

    for i in range(num_philosophers):
        philosopher = Philosopher(i, message_queues)
        philosophers.append(philosopher)
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()

if __name__ == '__main__':
    main()

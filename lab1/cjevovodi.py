import multiprocessing
import time
import random

class Message:
    def __init__(self, request_id: int, timestamp: int, tip: str):
        self.request_id = request_id  # ID zahtjeva
        self.timestamp = timestamp    # Logički sat
        self.tip = tip                # Tip poruke: "ZAH", "ODG"

    def __str__(self):
        return f"{self.tip}({self.request_id}, {self.timestamp})"


class Philosopher(multiprocessing.Process):
    def __init__(self, id, left_pipe, right_pipe):
        super().__init__()
        self.id = id
        self.local_time = random.randint(1, 500)
        self.left = False
        self.right = False
        self.lmessages = 0
        self.rmessages = 0
        self.left_pipe = left_pipe  # Cjevovod prema lijevom susjedu
        self.right_pipe = right_pipe  # Cjevovod prema desnom susjedu
        self.lodg = 0
        self.rodg = 0
        self.lzah = False
        self.rzah = False
        self.lizah = 0          #vrijednost lijevog zahtjeva
        self.rizah = 0          #vrijednost desnog zahtjeva
        self.lindex = (id - 1) % 5
        self.rindex = (id + 1) % 5

    def run(self):
        print(f"Filozof {self.id} ima vrijednost logičkog sata {self.local_time}.")
        while True:
            print(f"Filozof {self.id} misli...")
            time.sleep(random.uniform(6, 14))  # Simuliramo vrijeme razmišljanja
            # Šalje zahtjeve za štapiće
            if not self.lzah:
                mess = Message(self.id, self.local_time, "ZAH")
                print(f"Filozof {self.id} šalje poruku filozofu {self.lindex}: {mess}")
                self.left_pipe.send(mess)
                self.lzah = True                    #zahtjev
                self.lizah = self.local_time        #vrijednost zahtjeva

            if not self.rzah:
                mess = Message(self.id, self.local_time, "ZAH")
                print(f"Filozof {self.id} šalje poruku filozofu {self.rindex}: {mess}")
                self.right_pipe.send(mess)
                self.rzah = True                    #zahtjev
                self.rizah = self.local_time        #vrijednost zahtjeva

            # Prima poruku od susjeda
            if self.left_pipe.poll():
                msg = self.left_pipe.recv()
                self.handle_message(msg, "left")

            if self.right_pipe.poll():
                msg = self.right_pipe.recv()
                self.handle_message(msg, "right")

            if self.left and self.right:
                print(f"Filozof {self.id} jede...")
                time.sleep(random.uniform(6, 14))  # Simuliramo vrijeme jedenja
                self.release_sticks()
                self.reset()
                responsel = Message(self.id, self.lmessages, "ODG")
                responser = Message(self.id, self.rmessages, "ODG")
                self.left_pipe.send(responsel)
                self.right_pipe.send(responser)

    def handle_message(self, msg, direction):
        print(f"Filozof {self.id} prima poruku: {msg}")
        if msg.tip == "ZAH":
            self.local_time = max(self.local_time, msg.timestamp) + 1
            if direction == "left":
                self.lmessages = msg.timestamp
                if(self.lizah >= msg.timestamp):
                    response = Message(self.id, msg.timestamp, "ODG")
                    self.left_pipe.send(response)
                    print(f"Filozof {self.id} šalje odgovor filozofu {self.lindex}: {response}")
                    self.left = False
                    self.lodg = 1
                else:
                    self.left = True
            else:
                self.rmessages = msg.timestamp
                if(self.rizah > msg.timestamp):
                    response = Message(self.id, msg.timestamp, "ODG")
                    self.right_pipe.send(response)
                    print(f"Filozof {self.id} šalje odgovor filozofu {self.rindex}: {response}")
                    self.right = False
                    self.rodg = 1
                else:
                    self.right = True
        if msg.tip == "ODG":
            if direction == "left" and self.lodg == 0:
                self.left = True
            if direction == "right" and self.rodg == 0:
                self.right = True
            if direction == "left" and self.lodg == 1:
                self.left = True
                self.lodg == 0
            if direction == "right" and self.rodg == 1:
                self.right = True
                self.rodg == 0

    def release_sticks(self):
        """
        Šalje poruke o oslobađanju štapića susedima.
        """
        print(f"Filozof {self.id} oslobađa štapiće.")

    def reset(self):
        self.left = False
        self.right = False
        self.lzah = False
        self.rzah = False
        self.lodg = 0
        self.rodg = 0


def create_pipes(num_philosophers):
    """
    Kreira parove cjevovoda između susednih filozofa.
    """
    pipes = []
    for i in range(num_philosophers):
        left_pipe, right_pipe = multiprocessing.Pipe()
        pipes.append((left_pipe, right_pipe))
    return pipes


def main():
    num_philosophers = 5
    pipes = create_pipes(num_philosophers)

    # Kreiramo filozofe sa povezanim cjevovodima
    philosophers = []
    for i in range(num_philosophers):
        left_pipe = pipes[i][0]
        right_pipe = pipes[(i + 1) % num_philosophers][1]
        philosopher = Philosopher(i, left_pipe, right_pipe)
        philosophers.append(philosopher)
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()


if __name__ == '__main__':
    main()

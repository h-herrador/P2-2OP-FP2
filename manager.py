from queues import ArrayQueue, ExecutionQueue
from process import Process
import sys
import pandas as pd
from prettytable import PrettyTable

class QueueManager:
    def __init__(self):
        self.register_queue = ArrayQueue()
        self.cpu_short = ExecutionQueue(resource = "cpu", estimated_time = "short")
        self.cpu_long = ExecutionQueue(resource = "cpu", estimated_time = "long")
        self.gpu_short = ExecutionQueue(resource = "gpu", estimated_time = "short")
        self.gpu_long = ExecutionQueue(resource = "gpu", estimated_time = "long")
        self.penalized_users = set()
        self.current_time = 0
        self.current_processes = {("cpu", "short"): None,
                                  ("cpu", "long"): None,
                                  ("gpu", "short"): None, 
                                  ("gpu", "long"): None
                                 }
        self.stats_penalties = []
        self.stats_time = []


    def read_file(self):
        try:
            file = input(f"Por favor indique a continuación el nombre del archivo que quiere leer: \nNombre del archivo: ").strip().lower()
            with open(file) as txt:
                reader = txt.read()
                for line in reader.split("\n"):
                    if line:
                        data = line.split()
                        if len(data) == 5:
                            process = Process(process_id = data[0], user_id = data[1], resource = data[2], estimated_time = data[3], execution_time = int(data[4]))
                            self.register_queue.enqueue(process)
                            
                print(f"El fichero ha sido leído con éxito. {len(self.register_queue)} procesos han sido añadidos.")
        
        except FileNotFoundError:
            print("El fichero no se ha encontrado. Por favor inténtalo de nuevo más tarde.")
            sys.exit()


    def enqueue(self, p: Process):
        match p.resource, p.estimated_time:
            case "cpu", "short":
                self.cpu_short.enqueue(p)

            case "cpu", "long":
                self.cpu_long.enqueue(p) 
            
            case "gpu", "short":
                self.gpu_short.enqueue(p) 
            
            case "gpu", "long":
                self.gpu_long.enqueue(p)


    def simulate(self):
        while any([not(self.cpu_short.is_empty()), not(self.cpu_long.is_empty()), not(self.gpu_short.is_empty()), not(self.gpu_long.is_empty()), not(self.register_queue.is_empty())]) or any(self.current_processes.values()):
            self.current_time += 1

            if not(self.register_queue.is_empty()):
                p = self.register_queue.dequeue()
                p.entry_time = self.current_time
                self.enqueue(p)
                print(f"Proceso añadido a cola de ejecución:\n\tTiempo actual: {self.current_time}\n\tID Proceso: {p.process_id}\n\tID Usuario: {p.user_id}\n\tTipo de recurso: {p.resource}\n\tTiempo estimado: {p.estimated_time}\n")


            for q, p in filter(lambda x: bool(x[1]),self.current_processes.items()): # Checking if any processes are over
                if p.is_over(self.current_time):
                    self.current_processes[q] = None
                    print(f"Proceso terminado:\n\tTiempo actual: {self.current_time}\n\tID Proceso: {p.process_id}\n\tID Usuario: {p.user_id}\n\tTipo de recurso: {q[0]}\n\tTiempo estimado: {q[1]}\n\tTiempo de entrada: {p.entry_time}\n\tTiempo de inicio de ejecución: {p.start_time}\n\tTiempo de ejecución: {p.execution_time}\n")

                    if q[1] == "short" and p.execution_time > 5: # Checking if we should penalize the user
                        self.penalized_users.add(p.user_id)
                        print(f"Penalización activa:\n\tTiempo actual: {self.current_time}\n\tID Usuario: {p.user_id}\n")


            for execution_queue in [i for i in (self.cpu_short, self.cpu_long, self.gpu_short, self.gpu_long) if not(i.is_empty())]:
                resource = execution_queue.resource
                time = execution_queue.estimated_time

                if not(self.current_processes[(resource, time)]):
                    p = execution_queue.dequeue()
                    self.stats_penalties.append([p.user_id, p.process_id, True if p.user_id in self.penalized_users else False])

                    if p.user_id in self.penalized_users: # Apply penalty
                        self.penalized_users.remove(p.user_id)
                        print(f"Penalización aplicada:\n\tTiempo actual: {self.current_time}\n\tID Proceso: {p.process_id}\n\tID Usuario: {p.user_id}\n")
                        if p.resource == "cpu":
                            self.cpu_long.enqueue(p)
                            print(f"Proceso añadido a cola de ejecución:\n\tTiempo actual: {self.current_time}\n\tID Proceso: {p.process_id}\n\tID Usuario: {p.user_id}\n\tTipo de recurso: cpu\n\tTiempo estimado: long\n")

                        else:
                            self.gpu_long.enqueue(p)
                            print(f"Proceso añadido a cola de ejecución:\n\tTiempo actual: {self.current_time}\n\tID Proceso: {p.process_id}\n\tID Usuario: {p.user_id}\n\tTipo de recurso: gpu\n\tTiempo estimado: long\n")

                    else:
                        self.current_processes[(resource, time)] = p # Start the execution 
                        p.start_time = self.current_time
                        self.stats_time.append([(resource, time), p.process_id, p.start_time - p.entry_time])


    def show_stats(self):
        print()
        df_penalties = pd.DataFrame(self.stats_penalties, columns = ["user", "process", "penalty"]).drop_duplicates(subset = ["process"], keep = "first")
        df_time = pd.DataFrame(self.stats_time, columns = ["queue", "process", "time"]).drop_duplicates(keep = "last")

        group_col = "user"
        target_col = "penalty"
        stats = df_penalties.groupby(group_col).agg({target_col: ["mean"]})
        table = PrettyTable()
        table.field_names = ["queue", "penalties"]

        for row in stats.itertuples():
            user, penalty = row
            table.add_row((user, f"{penalty:.4f}"))
        print(table)


        group_col = "queue"
        target_col = "time"
        stats = df_time.groupby(group_col).agg({target_col: ["mean"]})
        table = PrettyTable()
        table.field_names = ["queue", "time"]

        for row in stats.itertuples():
            user, time = row
            table.add_row((f"{user[0]} {user[1]}", f"{time:.4f}"))
        print(table)
        
        
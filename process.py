from queues import *

class Process():
    def __init__(self, process_id, user_id, resource, estimated_time, execution_time):
        self.process_id = process_id
        self.user_id = user_id
        self.resource = resource 
        self.estimated_time = estimated_time
        self.execution_time = execution_time
        self.start_time = False
        self.entry_time = False
    

    @property
    def process_id(self):
        return self._process_id 
    
    @process_id.setter
    def process_id(self, process_id):
        if isinstance(process_id, str) and len(process_id) == 8:
            self._process_id = process_id

        else:
            raise(ValueError("Invalid process id"))


    @property 
    def user_id(self):
        return self._user_id
    
    @user_id.setter 
    def user_id(self, user_id):
        if all((isinstance(user_id, str), len(user_id) == 8, user_id.startswith("user"))):
            self._user_id = user_id
        
        else:
            raise(ValueError("Invalid user id"))

    
    @property 
    def resource(self):
        return self._resource 
    
    @resource.setter 
    def resource(self, resource):
        if resource in ("cpu", "gpu"):
            self._resource = resource
        
        else:
            raise(ValueError("Invalid resource type")) 
    
    
    @property 
    def estimated_time(self):
        return self._estimated_time

    @estimated_time.setter
    def estimated_time(self, estimated_time):
        if estimated_time in ("short", "long"):
            self._estimated_time = estimated_time
        
        else:
            raise(ValueError("Invalid estimated execution time"))


    @property
    def execution_time(self):
        return self._execution_time
    
    @execution_time.setter
    def execution_time(self, execution_time):
        if isinstance(execution_time, int) and execution_time > 0:
            self._execution_time = execution_time
        
        else:
            raise(ValueError("Invalid execution time"))


    @property 
    def start_time(self):
        return self._start_time
    
    @start_time.setter 
    def start_time(self, start_time):
        if (isinstance(start_time, int) and start_time >= 0) or start_time == False:
            self._start_time = start_time

        else:
            raise(ValueError("Invalid start time"))

    @property 
    def entry_time(self):
        return self._entry_time
    
    @entry_time.setter 
    def entry_time(self, entry_time):
        if (isinstance(entry_time, int) and entry_time >= 0) or entry_time == False:
            self._entry_time = entry_time

        else:
            raise(ValueError("Invalid entry time"))
        
    
    def is_over(self, time):
        return time >= self.start_time + self.execution_time
        
if __name__ == "__main__":
    pass
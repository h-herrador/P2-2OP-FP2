from queues import *

class Process:
    """
    Represents a process in the system.

    Attributes:
        process_id (str): Unique identifier for the process (must be 8 characters long).
        user_id (str): User identifier (must start with "user" and be 8 characters long).
        resource (str): Resource required by the process (must be "cpu" or "gpu").
        estimated_time (str): Estimated execution time (must be "short" or "long").
        execution_time (int): Execution time of the process in seconds (must be greater than 0).
        start_time (int/bool): Start time of the process in seconds (must be a non-negative integer or False).
        entry_time (int/bool): Entry time of the process in seconds (must be a non-negative integer or False).
    """

    def __init__(self, process_id, user_id, resource, estimated_time, execution_time):
        """
        Initializes a new instance of the Process class.

        Args:
            process_id (str): Unique identifier for the process.
            user_id (str): User identifier.
            resource (str): Resource required by the process.
            estimated_time (str): Estimated execution time.
            execution_time (int): Execution time of the process in seconds.
        """
        self.process_id = process_id
        self.user_id = user_id
        self.resource = resource 
        self.estimated_time = estimated_time
        self.execution_time = execution_time
        self.start_time = False
        self.entry_time = False

    @property
    def process_id(self):
        """Gets the process identifier."""
        return self._process_id 
    
    @process_id.setter
    def process_id(self, process_id):
        """Sets the process identifier."""
        if isinstance(process_id, str) and len(process_id) == 8:
            self._process_id = process_id
        else:
            raise ValueError("Invalid process id")

    @property 
    def user_id(self):
        """Gets the user identifier."""
        return self._user_id
    
    @user_id.setter 
    def user_id(self, user_id):
        """Sets the user identifier."""
        if all((isinstance(user_id, str), len(user_id) == 8, user_id.startswith("user"))):
            self._user_id = user_id
        else:
            raise ValueError("Invalid user id")

    @property 
    def resource(self):
        """Gets the resource required by the process."""
        return self._resource 
    
    @resource.setter 
    def resource(self, resource):
        """Sets the resource required by the process."""
        if resource in ("cpu", "gpu"):
            self._resource = resource
        else:
            raise ValueError("Invalid resource type") 
    
    @property 
    def estimated_time(self):
        """Gets the estimated execution time of the process."""
        return self._estimated_time

    @estimated_time.setter
    def estimated_time(self, estimated_time):
        """Sets the estimated execution time of the process."""
        if estimated_time in ("short", "long"):
            self._estimated_time = estimated_time
        else:
            raise ValueError("Invalid estimated execution time")

    @property
    def execution_time(self):
        """Gets the execution time of the process in seconds."""
        return self._execution_time
    
    @execution_time.setter
    def execution_time(self, execution_time):
        """Sets the execution time of the process in seconds."""
        if isinstance(execution_time, int) and execution_time > 0:
            self._execution_time = execution_time
        else:
            raise ValueError("Invalid execution time")

    @property 
    def start_time(self):
        """Gets the start time of the process in seconds."""
        return self._start_time
    
    @start_time.setter 
    def start_time(self, start_time):
        """Sets the start time of the process in seconds."""
        if (isinstance(start_time, int) and start_time >= 0) or start_time == False:
            self._start_time = start_time
        else:
            raise ValueError("Invalid start time")

    @property 
    def entry_time(self):
        """Gets the entry time of the process in seconds."""
        return self._entry_time
    
    @entry_time.setter 
    def entry_time(self, entry_time):
        """Sets the entry time of the process in seconds."""
        if (isinstance(entry_time, int) and entry_time >= 0) or entry_time == False:
            self._entry_time = entry_time
        else:
            raise ValueError("Invalid entry time")
        
    def is_over(self, time):
        """
        Determines if the process has finished.

        Args:
            time (int): The current time in seconds.

        Returns:
            bool: True if the process has finished, False otherwise.
        """
        return time >= self.start_time + self.execution_time
        
if __name__ == "__main__":
    pass

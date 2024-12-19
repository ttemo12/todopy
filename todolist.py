import sys
from typing import List

class Task:
    def __init__(self, description: str, completed: bool = False):
        self.description = description
        self.completed = completed
    
    def to_string(self) -> str:
        return f"{self.description},{self.completed}"
    
    def __repr__(self) -> str:
        return f"Task(description='{self.description}', completed={self.completed})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return self.description == other.description and self.completed == other.completed

def add_task(todo_list: List[Task], desc: str) -> None:
    task = Task(description=desc)
    todo_list.append(task)
    print(f"added: {desc}")

def complete_task(todo_list: List[Task], desc: str) -> None:
    found = False
    for task in todo_list:
        if task.description == desc:
            task.completed = True
            print(f"Task completed: {task.description}")
            found = True
            break
    
    if not found:
        print(f"Task not found: {desc}")

def list_tasks(todo_list: List[Task]) -> None:
    if not todo_list:
        print("No tasks found.", file=sys.stderr)
    else:
        print("Tasks:")
        for i, task in enumerate(todo_list, 1):
            status = "[X]" if task.completed else "[ ]"
            print(f"{i}: {status} - {task.description}")

def save_to_file(todo_list: List[Task]) -> None:
    try:
        with open("todo_list.txt", "w") as file:
            for task in todo_list:
                file.write(f"{task.to_string()}\n")
    except IOError as e:
        print(f"Unable to save tasks to file: {e}")

def load_from_file() -> List[Task]:
    todo_list = []
    try:
        with open("todo_list.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 2:
                        description = parts[0]
                        completed = parts[1].lower() == "true"
                        todo_list.append(Task(description=description, completed=completed))
    except FileNotFoundError:
        pass 
    return todo_list

def main():
    todo_list = load_from_file()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "add" and len(sys.argv) > 2:
            description = sys.argv[2]
            add_task(todo_list, description)
            save_to_file(todo_list)
        elif command == "complete" and len(sys.argv) > 2:
            description = sys.argv[2]
            complete_task(todo_list, description)
            save_to_file(todo_list)
        elif command == "list":
            list_tasks(todo_list)
        else:
            print("unknown command or invalid syntax")
    else:
        print("enter valid syntax (python todo.py [command] [description])")


if __name__ == "__main__":
    main()
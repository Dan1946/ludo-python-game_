import json

CONTACT_FILE_PATH = "tasks.json"


class Task:
    max_content_capacity = 200

    def __init__(self, max_content_capacity):
        self.max_content_capacity = max_content_capacity

    def read_tasks(self, file_path):
        try:
            with open(file_path, 'r') as f:
                tasks = json.load(f)['tasks']
        except FileNotFoundError:
            tasks = []

        return tasks

    def write_tasks(self, file_path, tasks):
        with open(file_path, 'w') as f:
            tasks = {"tasks": tasks}
            json.dump(tasks, f)
        
    def add_task(self, tasks):
        task = {}

        while True:
            task_name = input("Enter task name(compulsory): ")
            if task_name:
                break
        content = input("Enter task content: ")
        words = content.split()

        if len(words) > self.max_content_capacity:
            print("You have exceeded the content threshold. This task could not be added.")
            return

        task["name"] = task_name
        task["content"] = content
        task["completed"] = False
        tasks.append(task)
        print("Task saved!")
    
    def search_for_task(self, tasks):
        matching_tasks = []
        by_name_or_content = input("Do you want to search by name or content(n/c): ")

        if by_name_or_content == "n":
            task_name = input("Enter name of task: ")
            if task_name:
                for task in tasks:
                    if  task_name in task["name"]:
                        matching_tasks.append(task)
            
            else:
                print("You didn't enter a name. Search ended.")
                return
            
        elif by_name_or_content == "c":
            task_content = input("Enter content of task: ")

            if task_content:

                for task in tasks:  
                        if  task_content in task["content"]:
                            matching_tasks.append(task)

            else:
                print("You didn't enter any content. Search ended.")

        if len(matching_tasks) > 0:
            self.list_tasks(matching_tasks)

    def list_tasks(self, tasks):
        # tasks.sort(reverse = True)

        print("---------Tasks---------")
        for i, task in enumerate(tasks):
            name = task["name"]
            content = task["content"]
            task["number_id"] = f"{i + 1}"
            if task["completed"]:
                print(f"{i + 1} Task_name: {name}(completed)")
            else:
                print(f"{i + 1} Task_name: {name}")
            print(f"  Task_content: {content}")
            print()
    
    def edit_task(self, tasks):
        edit = input("Would you like to edit any task (yes/no)? ").lower()
        if edit == "yes":
            print("1.Add content to task")
            print("2.Mark task as completed")
            print("3.Change task name")
            print("4.change content(over-writes current content)")

            num = input("Enter desired task number, press (q) to quit: ")

            if num  == "q":
                return
            
            if int(num) > len(tasks):
                    print('Invalid task number.')
                    return
            
            for task in tasks:
                if task["number_id"] == num:
                    mode = input("Enter any number from the operations above: ")

                    if mode == "1":
                        extra_content = input(f"{task['content']} ")
                        task["content"] += extra_content
                        print("Task updated!")
                    
                    elif mode == "2":
                        completed = input("Do you want to mark this task as completed(y/n): ")
                        if completed == "y":

                            if task["completed"]:
                                print("Sorry,this task has already been marked as completed.")
                                unmark = input("Do you want unmark this task (y/n)? ")
                                
                                if unmark.lower() == "y":
                                    task["completed"] = not task["completed"]
                                    print("Unmarked!")

                                else:
                                    break

                            else:
                                task["completed"] = not task["completed"]
                                print("Task marked as completed.")
                    
                    elif mode == "3":
                        new_name = input("Enter new name: ")

                        if new_name:
                            task["name"] = new_name
                            print("Task name updated!")

                        else:
                            print("No name was entered. Operation terminated.")

                    elif mode == "4":
                        new_content = input("")
                        task["content"] = new_content
                        print("Task updated!")
                 
                    else:
                        print("Invalid number.")
                        break

    def delete_task(self, tasks):
        task_id = input("Enter task number: ")
        
        for task in tasks:
            if task["number_id"] == task_id:
                tasks.remove(task)
                print("Task deleted!")

    def main(self, tasks_path):
        print("Welcome to your Task list!.")
        print("The following is a list of useable commands:")
        print("'add': Adds a task.")
        print("'delete': Deletes a task.")
        print("'list': Lists all tasks.")
        print("'edit': Allows editing of tasks.")
        print("'search': Searches for a task by name.")
        print("'q': Quits the program and saves all changes to the task list.")
        print()
        tasks = self.read_tasks(tasks_path)
        while True:
            command = input("Type a command: ").lower()
            if command == "q":
                break

            elif command == "add":
                self.add_task(tasks)

            elif command == "list":
                self.list_tasks(tasks)

            elif command == "search":
                self.search_for_task(tasks)

            elif command == "delete":
                self.delete_task(tasks)
            
            elif command == "edit":
                self.edit_task(tasks)

            else:
                print("Invalid command.")

        self.write_tasks(CONTACT_FILE_PATH, tasks)
        print("Tasks were saved successfully!")


t = Task(100)

if __name__ == "__main__":
    t.main(CONTACT_FILE_PATH)


                
                     
                







    
    
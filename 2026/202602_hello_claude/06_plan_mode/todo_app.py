"""Plan Mode Hello World用 - シンプルなTodoアプリ"""


class TodoApp:
    def __init__(self):
        self.tasks = []

    def add_task(self, title: str) -> dict:
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "done": False,
        }
        self.tasks.append(task)
        return task

    def complete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task["id"] == task_id:
                task["done"] = True
                return True
        return False

    def list_tasks(self) -> list:
        return self.tasks

    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                return True
        return False


if __name__ == "__main__":
    app = TodoApp()
    app.add_task("Claude Codeを学ぶ")
    app.add_task("Plan modeを試す")
    app.add_task("Hooksを設定する")
    app.complete_task(1)
    for task in app.list_tasks():
        status = "✓" if task["done"] else "○"
        print(f"[{status}] {task['id']}. {task['title']}")

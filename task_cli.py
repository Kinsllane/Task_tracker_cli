import sys
import json
import os
import datetime

class TaskTracker():
    def __init__(self):
        self.tasks = []
        self.filename = 'tasks.json'
        self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из JSON-файла"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            else:
                self.tasks = []
                print("❌ Файл не найден, будет создан при сохранении")
                self.save_tasks()
        except json.JSONDecodeError:
            print(f"❌ Ошибка: Файл {self.filename} поврежден")
            self.tasks = []
        except Exception as e:
            print(f"❌ Ошибка при загрузке задач: {e}")
            self.tasks = []

    def save_tasks(self):
        """Сохрание задач в JSON-файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
            print(f"💾 Задачи сохранены в файл {self.filename}")
        except Exception as e:
            print(f"❌ Ошибка при сохранении задач: {e}")

    def get_next_id(self):
        if not self.tasks:
            return 1
        existing_ids = {task['id'] for task in self.tasks}
        new_id = 1
        while new_id in existing_ids:
            new_id = new_id + 1
        return new_id

    def add_task(self, description, status='todo'):
        if not description:
            print("❌ Ошибка: описание задачи не может быть пустым")
            return None
        new_id = self.get_next_id()

        createdAt = datetime.datetime.now().isoformat()
        updatedAt = createdAt

        new_task = {
            'id': new_id,
            'description': description.strip(),
            'status': status,
            'createdAt': createdAt,
            'updatedAt': updatedAt
        }

        self.tasks.append(new_task)

        self.save_tasks()

        print(f"✅ Задача успешно добавлена! (ID: {new_id})")
        return new_id


    def list_tasks(self, status_filter=None):
        """
            Показывает список задач
            status_filter: None - все задачи, 'todo', 'in-progress', 'done' - только по статусу
        """
        if status_filter:
            tasks_to_show = [task for task in self.tasks if task['status'] == status_filter]
            filter_text = f"со статусом '{status_filter}'"
        else:
            tasks_to_show = self.tasks
            filter_text = "все задачи"

        if not tasks_to_show:
            if status_filter:
                print(f"📭 Нет задач со статусом '{status_filter}'")
            else:
                print("📭 Список задач пуст")
            return

        print(f"\n📋 Список задач ({filter_text}):")
        print("-" * 50)

        for task in tasks_to_show:
            try:
                date_obj = datetime.datetime.fromisoformat(task['createdAt'])
                date_str = date_obj.strftime('%Y-%m-%d %H:%M')
            except (ValueError, TypeError):
                date_str = task['createdAt'][:16]

            status_emoji = {
                'todo': '⭕',
                'in-progress': '🔄',
                'done': '✅'
            }.get(task['status'], '📌')

            print(f"{status_emoji} ID: {task['id']} | [{task['status']}] {task['description']}")
            print(f"   📅 Создано: {date_str}")

            if task['updatedAt'] != task['createdAt']:
                try:
                    update_obj = datetime.datetime.fromisoformat(task['updatedAt'])
                    update_str = update_obj.strftime('%Y-%m-%d %H:%M')
                    print(f"   ✏️ Обновлено: {update_str}")
                except (ValueError, TypeError):
                    print(f"   ✏️ Обновлено: {task['updatedAt'][:16]}")

        print("-" * 50)

        tasks_count = len(tasks_to_show)
        if tasks_count == 1:
            print(f"📊 Показано: 1 задача")
        elif 2 <= tasks_count <= 4:
            print(f"📊 Показано: {tasks_count} задачи")
        else:
            print(f"📊 Показано: {tasks_count} задач")

        if status_filter and len(self.tasks) > tasks_count:
            total = len(self.tasks)
            if total == 1:
                print(f"📈 Всего в списке: 1 задача")
            elif 2 <= total <= 4:
                print(f"📈 Всего в списке: {total} задачи")
            else:
                print(f"📈 Всего в списке: {total} задач")



    def find_task(self,task_id):
        for task in self.tasks:
            if task['id'] == int(task_id):
                return task
        return None


    def update_task(self, task_id, new_description):
        if new_description:
            task = self.find_task(task_id)
            if task:
                task['description'] = new_description.strip()
                task['updatedAt'] = datetime.datetime.now().isoformat()
                self.save_tasks()
                print(f"✅ Задача #{task_id} обновлена:")
                return True
            print(f"❌ Задача с id: {task_id} - не найдена")
            return False

        else:
            print("❌ Ошибка: описание задачи не может быть пустым")
            return False

    def change_status(self, task_id, new_status):
        if new_status:
            task = self.find_task(task_id)
            if task:
                if new_status in ['todo', 'in-progress', 'done']:
                    task['status'] = new_status
                    task['updatedAt'] = datetime.datetime.now().isoformat()
                    self.save_tasks()
                    print(f"✅ Задача #{task_id} обновлена:")
                    return True
                print(f"❌ Неверный статус: {new_status}")
                return False
            print(f"❌ Задача с id: {task_id} - не найдена")
            return False

        else:
            print(f"❌ Ошибка: статус задачи не может быть пустым")
            return False

    def get_status_emoji(self, status):
        """Возвращает эмодзи для статуса"""
        emojis = {
            'todo': '⭕',
            'in-progress': '🔄',
            'done': '✅'
        }
        return emojis.get(status, '📌')

    def delete_task(self, task_id):
        """Удаляет задачу по ID"""
        task = self.find_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"🗑️ Задача #{task_id} удалена")
            return True
        print(f"❌ Задача с id: {task_id} не найдена")
        return False
def main():

    if len(sys.argv) < 2:
        print("❌ Неправильный формат ввода команды")
        return

    command = sys.argv[1]
    tracker = TaskTracker()

    match command:
        case 'add':
            if len(sys.argv) < 3:
                print("❌ Ошибка: не указано описание задачи")
                print("Использование: python task_cli.py add <описание> [статус]")
                return
            description = sys.argv[2]
            if len(sys.argv)>=4:
                status_filter = sys.argv[3]
                if status_filter in ['todo', 'in-progress', 'done']:
                    tracker.add_task(description, status_filter)
                else:
                    print(f"❌ Неверный статус: {status_filter}")
                    print("Доступные статусы: todo, in-progress, done")
            else:
                tracker.add_task(description)


        case 'list':
            ' task_cli.py list status'
            if len(sys.argv) < 3:
                tracker.list_tasks()
            else:
                status_filter = sys.argv[2]
                if status_filter in ['todo', 'in-progress', 'done']:
                    tracker.list_tasks(status_filter)
                else:
                    print(f"❌ Неверный статус: {status_filter}")
                    print("Доступные статусы: todo, in-progress, done")
                    print("Пример: python task_cli.py list todo")

        case 'update':
            if len(sys.argv) < 4:
                print("❌ Ошибка: не указаны ID задачи и новое описание")
                print("Использование: python task_cli.py update <id> <новое описание>")
                print("Пример: python task_cli.py update 1 \"Купить хлеб и молоко\"")
                return
            try:
                task_id = sys.argv[2]
                new_description = ' '.join(sys.argv[3:])
                tracker.update_task(task_id, new_description)
            except ValueError:
                print("❌ Ошибка: ID должен быть числом")
                print("Пример: python task_cli.py update 1 \"Новое описание\"")


        case 'mark-in-progress':
            if len(sys.argv) < 3:
                print("❌ Ошибка: не указан ID задачи")
                print("Использование: python task_cli.py mark-in-progress <id>")
                return

            try:
                task_id = int(sys.argv[2])
                tracker.change_status(task_id, 'in-progress')
            except ValueError:
                print("❌ Ошибка: ID должен быть числом")

        case 'mark-done':
            if len(sys.argv) < 3:
                print("❌ Ошибка: не указан ID задачи")
                print("Использование: python task_cli.py mark-done <id>")
                return

            try:
                task_id = int(sys.argv[2])
                tracker.change_status(task_id, 'done')
            except ValueError:
                print("❌ Ошибка: ID должен быть числом")

        case 'delete':
            if len(sys.argv) < 3:
                print("❌ Ошибка: не указан ID задачи")
                print("Использование: python task_cli.py delete <id>")
                return
            try:
                task_id = int(sys.argv[2])
                tracker.delete_task(task_id)
            except ValueError:
                print("❌ Ошибка: ID должен быть числом")


        case _:
            print(f"❌ Неизвестная команда: {command}")
            print("Доступные команды: add, list, update, delete, mark-in-progress, mark-done")






if __name__ == "__main__":
    main()
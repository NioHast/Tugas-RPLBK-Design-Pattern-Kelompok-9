import streamlit as st

class Task:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

class TaskManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskManager, cls).__new__(cls)
            cls._instance.tasks = []
            cls._instance.observers = []
        return cls._instance

    def add_task(self, task):
        self.tasks.append(task)
        self._notify_observers()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self._notify_observers()

    def _notify_observers(self):
        for observer in self.observers:
            observer.update(self.tasks)

    def register_observer(self, observer):
        self.observers.append(observer)

    def get_tasks(self):
        return self.tasks

class TaskObserver:
    def __init__(self):
        self._tasks = []

    def update(self, tasks):
        self._tasks = tasks
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []
        st.session_state.tasks = tasks

    def get_tasks(self):
        return self._tasks
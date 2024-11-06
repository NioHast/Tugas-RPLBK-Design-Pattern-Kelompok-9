import streamlit as st
from datetime import datetime
from task_manager import Task, TaskManager, TaskObserver

st.set_page_config(
    page_title="Pencatatan Tugas",
)

st.title("Website Pencatatan Tugas")
menu_choice = st.sidebar.radio("Pilih opsi:", ["Tambah Tugas", "Lihat & Hapus Tugas"])
task_manager = TaskManager()
observer = TaskObserver()
task_manager.register_observer(observer)

for key in ['tasks', 'due_dates']:
    if key not in st.session_state:
        st.session_state[key] = []

def add_task(title, due_date):
    task = Task(title, due_date)
    task_manager.add_task(task)
    st.session_state.due_dates.append(due_date)

def delete_task(index):
    if 0 <= index < len(st.session_state.tasks):
        task_manager.delete_task(index)
        return True
    return False

if menu_choice == "Tambah Tugas":
    st.subheader("Tambah Tugas")
    task_input = st.text_input("Masukkan tugas:")
    due_date_input = st.date_input("Batas waktu (Tanggal):")
    due_time_input = st.time_input("Batas waktu (Jam):")
    due_datetime = datetime.combine(due_date_input, due_time_input)

    if st.button("Tambah Tugas"):
        if task_input:
            add_task(task_input, due_datetime)
            st.success(f"Berhasil ditambahkan: '{task_input}' ({due_datetime}).")
        else:
            st.error("Silakan masukkan tugas yang valid.")

elif menu_choice == "Lihat & Hapus Tugas":
    st.subheader("Daftar Tugas")
    tasks = st.session_state.tasks
    if tasks:
        for idx, task in enumerate(tasks, 1):
            st.success(f"{idx}. {task.title} ({task.due_date})")
        
        st.subheader("Hapus Tugas")
        task_num = st.number_input("Pilih nomor tugas yang ingin dihapus:", min_value=1, max_value=len(tasks), step=1)
        
        if st.button("Hapus Tugas"):
            if delete_task(task_num - 1):
                st.success(f"Tugas nomor {task_num} berhasil dihapus.")
                st.session_state.tasks = task_manager.get_tasks()
            else:
                st.error("Nomor tugas tidak valid.")
    else:
        st.write("Tidak ada tugas yang tersedia untuk dihapus.")

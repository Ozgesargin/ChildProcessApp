# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 19:44:07 2024

@author: sargin
"""

import os
import sys
import time

def create_file(file_name):
    print(f"Dosya '{file_name}' olu�turuluyor...")
    with open(file_name, "w") as f:
        f.write("")

    print(f"Dosya '{file_name}' olu�turuldu.")
    sys.exit(0)

def write_file(file_name, data):
    print(f"'{file_name}' dosyas�na veri ekleniyor...")
    time.sleep(1)  # Dosya olu�turulma i�lemi i�in bekleme
    with open(file_name, "a") as f:
        f.write(data + "\n")
    print(f"'{file_name}' dosyas�na veri eklendi.")
    sys.exit(0)

def read_file(file_name):
    print(f"'{file_name}' dosyas� okunuyor...")
    time.sleep(2)  # Dosyaya veri eklenmesi i�in bekleme
    try:
        with open(file_name, "r") as f:
            content = f.read()
        print(f"'{file_name}' dosyas�n�n i�eri�i:\n{content}")
    except FileNotFoundError:
        print(f"Hata: '{file_name}' dosyas� bulunamad�.")
    sys.exit(0)

def main():
    # Kullan�c�dan giri� alma
    file_name = input("Olu�turulacak dosyan�n ad�n� giriniz: ").strip()
    data = input("Dosyaya eklenecek veriyi giriniz: ").strip()

    # 3 child process olu�turma
    processes = []
    try:
        for i, task in enumerate([
            lambda: create_file(file_name),  # �lk child process: Dosya olu�turma
            lambda: write_file(file_name, data),  # �kinci child process: Dosyaya veri ekleme
            lambda: read_file(file_name)  # ���nc� child process: Dosyay� okuma
        ]):
            pid = os.fork()
            if pid == 0:  # Child process
                task()
            else:  # Parent process
                processes.append(pid)

        # Parent process t�m child process'lerin tamamlanmas�n� bekler
        for pid in processes:
            completed_pid, status = os.wait()
            if os.WIFEXITED(status):
                print(f"Parent: Child process {completed_pid} normal sonland�. ��k�� durumu: {os.WEXITSTATUS(status)}")
            elif os.WIFSIGNALED(status):
                print(f"Parent: Child process {completed_pid} bir sinyal ile sonland�. Sinyal numaras�: {os.WTERMSIG(status)}")
    except OSError as e:
        print(f"Fork hatas�: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

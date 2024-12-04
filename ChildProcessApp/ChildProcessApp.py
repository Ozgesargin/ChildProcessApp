# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 19:44:07 2024

@author: sargin
"""

import os
import sys
import time

def create_file(file_name):
    print(f"Dosya '{file_name}' oluþturuluyor...")
    with open(file_name, "w") as f:
        f.write("")

    print(f"Dosya '{file_name}' oluþturuldu.")
    sys.exit(0)

def write_file(file_name, data):
    print(f"'{file_name}' dosyasýna veri ekleniyor...")
    time.sleep(1)  # Dosya oluþturulma iþlemi için bekleme
    with open(file_name, "a") as f:
        f.write(data + "\n")
    print(f"'{file_name}' dosyasýna veri eklendi.")
    sys.exit(0)

def read_file(file_name):
    print(f"'{file_name}' dosyasý okunuyor...")
    time.sleep(2)  # Dosyaya veri eklenmesi için bekleme
    try:
        with open(file_name, "r") as f:
            content = f.read()
        print(f"'{file_name}' dosyasýnýn içeriði:\n{content}")
    except FileNotFoundError:
        print(f"Hata: '{file_name}' dosyasý bulunamadý.")
    sys.exit(0)

def main():
    # Kullanýcýdan giriþ alma
    file_name = input("Oluþturulacak dosyanýn adýný giriniz: ").strip()
    data = input("Dosyaya eklenecek veriyi giriniz: ").strip()

    # 3 child process oluþturma
    processes = []
    try:
        for i, task in enumerate([
            lambda: create_file(file_name),  # Ýlk child process: Dosya oluþturma
            lambda: write_file(file_name, data),  # Ýkinci child process: Dosyaya veri ekleme
            lambda: read_file(file_name)  # Üçüncü child process: Dosyayý okuma
        ]):
            pid = os.fork()
            if pid == 0:  # Child process
                task()
            else:  # Parent process
                processes.append(pid)

        # Parent process tüm child process'lerin tamamlanmasýný bekler
        for pid in processes:
            completed_pid, status = os.wait()
            if os.WIFEXITED(status):
                print(f"Parent: Child process {completed_pid} normal sonlandý. Çýkýþ durumu: {os.WEXITSTATUS(status)}")
            elif os.WIFSIGNALED(status):
                print(f"Parent: Child process {completed_pid} bir sinyal ile sonlandý. Sinyal numarasý: {os.WTERMSIG(status)}")
    except OSError as e:
        print(f"Fork hatasý: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

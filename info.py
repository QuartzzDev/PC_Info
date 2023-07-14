# QuartzzDev

import subprocess
import sys
import cpuinfo
import platform
import psutil

cevap = int(input("""Detaylı Sonuç İçin [1] \nDaha Basit Sonuçlar İçin [2] """))

if (cevap == 1):
    msinfo_output = subprocess.check_output('msinfo32.exe /report msinfo_output.txt', shell=True)
    pc_info_output = subprocess.check_output('wmic computersystem get /format:list', shell=True)
    task_manager_output = subprocess.check_output('tasklist /v /fo csv', shell=True)

    with open('bilgisayar_bilgileri.txt', 'w') as f:
        f.write("MSInfo32 Bilgileri:\n\n")
        f.write(msinfo_output.decode('utf-8'))

        f.write("\n\nPC Özellikleri:\n\n")
        f.write(pc_info_output.decode('utf-8'))

        f.write("\n\nGörev Yöneticisi Bilgileri:\n\n")
        f.write(task_manager_output.decode('utf-8'))

    print("bilgisayar_bilgileri.txt -- msinfo_output.txt --> Dosyalarına Bakınız . .")
elif (cevap == 2):
    print("basitbilgi.txt Dosyası Oluşturuldu")
    def get_cpu_info():
        cpu_info = {}
        cpu_info['Model'] = platform.processor()
        cpu_info['Sayı'] = psutil.cpu_count(logical=False)
        cpu_info['Thread'] = psutil.cpu_count(logical=True)
        cpu_info['Frekans'] = psutil.cpu_freq().current
        cpu_info['Yüzde'] = psutil.cpu_percent(interval=1)
        return cpu_info

    def get_memory_info():
        memory_info = {}
        memory = psutil.virtual_memory()
        memory_info['Toplam'] = convert_to_gb(memory.total)
        memory_info['Kullanılan'] = convert_to_gb(memory.used)
        memory_info['Boşta'] = convert_to_gb(memory.available)
        memory_info['Yüzde'] = memory.percent
        return memory_info

    def get_disk_info():
        disk_info = {}
        partitions = psutil.disk_partitions()
        for partition in partitions:
            partition_name = partition.mountpoint
            disk_usage = psutil.disk_usage(partition_name)
            disk_info[partition_name] = {
                'Dosya Sistemi': partition.fstype,
                'Toplam': convert_to_gb(disk_usage.total),
                'Kullanılan': convert_to_gb(disk_usage.used),
                'Boşta': convert_to_gb(disk_usage.free),
                'Yüzde': disk_usage.percent
            }
        return disk_info

    def convert_to_gb(bytes):
        gb = bytes / (1024 ** 3)
        return round(gb, 2)

    def get_network_info():
        network_info = {}
        network_info['İsim'] = platform.node()
        network_info['IP'] = psutil.net_if_addrs()
        network_info['Bağlantı'] = psutil.net_connections()
        return network_info

    def main():
        os_info = {
            'İşletim Sistemi': platform.platform(),
            'Sürüm': platform.version()
        }

        cpu_info = get_cpu_info()
        memory_info = get_memory_info()
        disk_info = get_disk_info()
        network_info = get_network_info()

        with open('basitbilgi.txt', 'w') as file:
            file.write("İşletim Sistemi Bilgileri:\n")
            for key, value in os_info.items():
                file.write(f'{key}: {value}\n')
            file.write("\n")

            file.write("CPU Bilgileri:\n")
            for key, value in cpu_info.items():
                file.write(f'{key}: {value}\n')
            file.write("\n")

            file.write("Bellek Bilgileri:\n")
            for key, value in memory_info.items():
                file.write(f'{key}: {value}\n')
            file.write("\n")

            file.write("Disk Bilgileri:\n")
            for partition, partition_info in disk_info.items():
                file.write(f'Partition: {partition}\n')
                for key, value in partition_info.items():
                    file.write(f'{key}: {value}\n')
                file.write("\n")

            file.write("Ağ Bilgileri:\n")
            for key, value in network_info.items():
                file.write(f'{key}: {value}\n')
            file.write("\n")

    if __name__ == '__main__':
        main()

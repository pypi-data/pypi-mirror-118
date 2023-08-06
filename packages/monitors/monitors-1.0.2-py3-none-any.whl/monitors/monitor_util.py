# -*- coding: utf-8 -*-

import os
import datetime
import socket
import time
import psutil
from influxdb import InfluxDBClient

from monitors.monitor_set import Settings as ST
from monitors.monitor_pid import get_process_id

client = InfluxDBClient(host=ST.host, port=ST.port, username=ST.username, password=ST.password, database=ST.database)


def monitor(process_id):
    """
    设定监控时间  默认1天
    :param process_id:
    :return:
    """

    try:
        CYCLE_TIME = datetime.timedelta(weeks=0, days=ST.monitor_duration, hours=00, minutes=0, seconds=5, microseconds=0,
                                        milliseconds=0)
        start_time = datetime.datetime.today()
        title = '时间' + "\t			  " + '运行状态' + "\t" + 'CPU百分比' + " " + '内存利用率' + "\t" + '虚拟内存' + "\t" + '实际使用内存' + "\t" + '网络发送包' + " " + '网络接受包' + "\n"
        print(title)
        if psutil.pid_exists(process_id):
            p = psutil.Process(process_id)
            pName = p.name()
            logName = pName + "_" + str(process_id) + "_stress_monitoring_record.log"
            print(logName + '\n')
            if not os.path.exists(ST.monitor_log_path):
                os.mkdir(ST.monitor_log_path)
            logfile = open(ST.monitor_log_path + '/' + logName, "a")
        else:
            print("pid is not exists please enter true pid!!!")
            return
        wTime = ST.refresh_interval
        
        while True:
            if datetime.datetime.today() - start_time > CYCLE_TIME:
                break
            recTime = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))

            if psutil.pid_exists(process_id):
                try:
                    status = p.status()
                    pCpu = u'%.2f' % (p.cpu_percent(interval=1))
                    mem = u'%.4f' % (p.memory_percent())
                    vmm = p.memory_info().vms
                    mm = p.memory_info().rss
                    net_sent = psutil.net_io_counters().packets_sent
                    net_recv = psutil.net_io_counters().packets_recv
                    monitor_content = str(recTime) + "\t" + str(status) + "\t" + str(pCpu) + '%' + "\t" + str(mem) + '%' + "\t" + str(
                        vmm) + "\t" + str(mm) + "\t" + str(net_sent) + "\t" + str(net_recv) + "\n"
                    print(monitor_content)
                    logfile.flush()
                    logfile.write(monitor_content)
                except Exception as e:
                    print('监控结束：{}'.format(e))
                    pass
            else:
                monitor_content = str(datetime.datetime.today()) + "\t" + str(process_id) + "  is not running!!!!!!!!!\n"
                print(monitor_content)
                logfile.flush()
                logfile.write(monitor_content)
                break

            time.sleep(wTime)

        logfile.close()
    except ProcessLookupError as e:
        print('监控结束：{}'.format(e))
        pass


def monitor_start(name):
    try:
        pid = int(get_process_id(process_name=name))
        monitor(pid)

    except TypeError as E:
        print('应用未启动 或 无此进程：{}'.format(E))


def get_host_ip():
    """
    获取本机ip
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(('8.8.8.8', 80))
        host_ip = s.getsockname()[0]
    finally:
        s.close()

    return host_ip


def monitor_view():
    """
    设定监控时间  默认1天
    :return:
    """

    try:
        CYCLE_TIME = datetime.timedelta(weeks=0, days=ST.monitor_duration, hours=00, minutes=0, seconds=5,
                                        microseconds=0,
                                        milliseconds=0)
        start_time = datetime.datetime.today()
        ip = get_host_ip()

        wTime = ST.refresh_interval

        while True:
            if datetime.datetime.today() - start_time > CYCLE_TIME:
                break

            try:
                cpu_info = [
                    {
                        "measurement": "{}_cpu_info".format(ST.table),
                        "tags": {
                            "host": ip
                        },
                        "fields": {
                            "percent": psutil.cpu_percent(0)
                        }
                    }
                ]
                memory_info = [
                    {
                        "measurement": "{}_memory_info".format(ST.table),
                        "tags": {
                            "host": ip
                        },
                        "fields": {
                            "mem_percent": psutil.virtual_memory().percent,
                            "mem_used": psutil.virtual_memory().used,
                            "mem_free": psutil.virtual_memory().free,
                        }
                    }
                ]
                disk_info = [
                    {
                        "measurement": "{}_disk_info".format(ST.table),
                        "tags": {
                            "host": ip
                        },
                        "fields": {
                            "disk_used": psutil.disk_usage('/').used,
                            "disk_free": psutil.disk_usage('/').free,
                            "disk_percent": psutil.disk_usage('/').percent,
                        }
                    }
                ]
                network_info = [
                    {
                        "measurement": "{}_network_info".format(ST.table),
                        "tags": {
                            "host": ip
                        },
                        "fields": {
                            "bytes_sent": psutil.net_io_counters().packets_sent,
                            "bytes_recv": psutil.net_io_counters().packets_recv,
                        }
                    }
                ]
                client.write_points(cpu_info)
                client.write_points(memory_info)
                client.write_points(disk_info)
                client.write_points(network_info)

            except Exception as e:
                print('End of monitoring：{}'.format(e))
                pass

            time.sleep(wTime)

    except ProcessLookupError as e:
        print('End of monitoring：{}'.format(e))
        pass


def monitor_on():
    try:
        monitor_view()

    except TypeError as E:
        print('监控服务启动异常：{}'.format(E))
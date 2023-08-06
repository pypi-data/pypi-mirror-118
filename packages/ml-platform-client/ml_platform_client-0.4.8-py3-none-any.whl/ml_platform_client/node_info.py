import psutil

from .service_response import success_response_with_data, format_service_response


class NodeInfo:
    unit = 1024 * 1024 * 1024

    def __init__(self):
        self.total_cpu = None
        self.total_memory = None
        self.idle_cpu_rate = None
        self.idle_memory_rate = None
        self.net_io = None
        self.block_io = None

    def get_memory(self):
        data = psutil.virtual_memory()
        self.total_memory = data.total / self.unit  # 总内存,单位为byte
        self.idle_memory_rate = round(data.available / data.total, 2)

    def get_cpu(self):
        self.total_cpu = psutil.cpu_count(logical=True)
        self.idle_cpu_rate = round((100 - psutil.cpu_percent(interval=1)) / 100, 2)

    def get_io(self):
        net_io = psutil.net_io_counters()
        self.net_io = (
            str(round(net_io.bytes_sent / self.unit, 1))
            + "/"
            + str(round(net_io.bytes_recv / self.unit, 1))
        )

        block_io = psutil.disk_io_counters()
        self.block_io = (
            str(round(block_io.read_bytes / self.unit, 1))
            + "/"
            + str(round(block_io.write_bytes / self.unit, 1))
        )

    def statistics(self):
        self.get_cpu()
        self.get_memory()
        self.get_io()
        result = {
            "totol_memory": self.total_memory,
            "totol_cpu": self.total_cpu,
            "idle_memory_rate": self.idle_memory_rate,
            "idle_cpu_rate": self.idle_cpu_rate,
            "net_io": self.net_io,
            "block_io": self.block_io,
        }
        return format_service_response(success_response_with_data(result))


node_info = NodeInfo()

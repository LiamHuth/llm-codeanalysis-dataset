#
#

class FileSystem:
    class Directory:
        def __init__(self):
            self.directory_map = {}

    def __init__(self):
        self.root = self.Directory()
        self.temp_pointer = self.root
        self.dir_in_path = []

    def pwd(self):
        path = "/"
        if not self.dir_in_path:
            return path
        else:
            for dir_name in self.dir_in_path:
                path += dir_name + "/"
            return path[:-1]

    def ls(self):
        path = self.pwd()
        self.temp_pointer = self.root
        if path != "/":
            arr = path.split("/")
            for name in arr[1:]:
                self.temp_pointer = self.temp_pointer.directory_map[name]
        return list(self.temp_pointer.directory_map.keys())

    def cd(self, path):
        # Taint Source: User input 'path'
        if path[0] != '/':
            path = self.pwd() + '/' + path
        arr = path.split("/")
        self.temp_pointer = self.root
        self.dir_in_path = []
        for name in arr[1:]:
            if name not in self.temp_pointer.directory_map:
                return
            self.temp_pointer = self.temp_pointer.directory_map[name]
            self.dir_in_path.append(name)

    def mkdir(self, path):
        # Taint Source: User input 'path'
        if path[0] != '/':
            path = self.pwd() + '/' + path
        arr = path.split("/")
        self.temp_pointer = self.root
        for name in arr[1:]:
            if name not in self.temp_pointer.directory_map:
                self.temp_pointer.directory_map[name] = self.Directory()
            self.temp_pointer = self.temp_pointer.directory_map[name]

    def rm(self, path):
        # Taint Source: User input 'path'
        if path[0] != '/':
            path = self.pwd() + '/' + path
        arr = path.split("/")
        self.temp_pointer = self.root
        for name in arr[1:-1]:
            self.temp_pointer = self.temp_pointer.directory_map[name]
        self.temp_pointer.directory_map.pop(arr[-1], None)

    def session_clear(self):
        self.temp_pointer = self.root
        self.dir_in_path = []

if __name__ == '__main__':
    fs = FileSystem()
    fs.mkdir("dir1")
    fs.cd("dir1")
    fs.mkdir("dir2")
    fs.cd("..")
    fs.rm("dir1")

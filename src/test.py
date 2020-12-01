from TEC_USB import MeerstetterTEC_USB
from TEC import MeerstetterTEC

def main():
    tec = MeerstetterTEC()
    print(tec.formReadCommand(0x0064, 1))
    print(tec.formReadCommand(0x0064, 1))



if __name__ == "__main__":
    main()
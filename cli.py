import speedtest
import pandas as pd
import time

def fetch_results():
    speedtester = speedtest.Speedtest()
    speedtester.get_best_server()
    speedtester.download()
    speedtester.upload()
    result_dict = speedtester.results.dict()
    return result_dict

def write_file(file_name,result_dict):
    file = open(file_name,'a')
    date = pd.to_datetime("today").strftime("%Y/%m/%d %H:%M:%S")
    file.write(date+';'+str(round(result_dict['download']/1024/1024,2))+';'
               +str(round(result_dict['upload']/1024/1024,2))+';'+str(round(result_dict['ping'],2))+'\n')
    file.close()

if __name__ == '__main__':
    start_time=time.time()
    print('---FETCHING SPEEDS---')
    result = fetch_results()
    write_file('/home/pi/net_speed/log.txt',result)
    print("--- %s seconds ---"% (time.time()-start_time))

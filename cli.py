import speedtest
speedtester = speedtest.Speedtest()
speedtester.get_best_server()
speedtester.download()
speedtester.upload()
results_dict = speedtester.results.dict()

#print results
print({'download':results_dict['download']/1024/1024,'upload':results_dict['upload']/1024/1024,'ping':results_dict['ping']})


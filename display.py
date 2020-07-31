import pandas as pd 
import time
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.express as px
import subprocess
import sys

def get_title(column):
    if column=="Download":
        return 'History for download speeds (Mb/s)'
    elif column=="Upload":
        return 'History for upload speeds (Mb/s)'
    else:
        return 'History of Ping'

def get_html(column,df):
    fig = px.line(df, x=df.index, y=column, title=get_title(column))
    fig.update_yaxes(rangemode="tozero")
    fig.update_traces(line_color='#000')
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=24, label="24h", step="hour", stepmode="todate"),
                dict(count=7, label="1w", step="day", stepmode="todate"),
                dict(count=14, label="2w", step="day", stepmode="todate"),
                dict(count=1, label="1m", step="month", stepmode="todate"),
                dict(count=6, label="6m", step="month", stepmode="todate"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all",label="All")
            ])
        )
    )
    fig.update_layout(template="simple_white")

    string = plotly.io.to_html(fig,full_html=False,include_plotlyjs=False)
    string=string.replace("\n", "")
    return(string)

def write_markup(df):
    ############################ CHANGE PATHS #######################
    path = '//home/pi/dijkstrar.github.io/_portfolio/speedtracker.md'
    title_md = "--- \ntitle: \'Internet Speedtracker\' \ndate: 2020-07-13 \npermalink: /portfolio/2020/07/plotly-html/ \n---\n\n"
    update_date_md = "History of internet speed tests, updated at: "+str(pd.to_datetime("today").strftime("%Y/%m/%d %H:%M")+"\n\n")
    body_md = "This is a dynamically updating web page. Internet speeds (download, upload and ping) get measured at a regular interval on a Raspberry Pi3b. Measurements of these speeds takes place via <https://speedtest.net> with the help of the [speedtest-cli package](https://pypi.org/project/speedtest-cli/).\n\n The measured speeds get recorded and displayed in the plots below. Ziggo (ISP) promises to deliver speeds of 100MB/s download, and upload. Whenever these speeds are not obtained, Ziggo will be automatically notified via twitter [@renzecodes](https://twitter.com/renzecodes). A history of download, upload speeds and ping are displayed in the Figures below, the history of internet speeds will be used to detect anomalies. Plots are created with the help of [Plotly package](https://plotly.com). Full code available on <https://github.com/dijkstrar/net_speed> \n"
    javascript_md = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script> \n'
    try:
        with open(path,'w') as f:
            f.write(title_md)
            f.write(update_date_md)
            f.write(body_md)
            f.write(javascript_md)
            for col in df.columns:
                f.write(get_html(col,df))
                f.write("\n\n")
        f.close()
    except:
        print('Error occurred in Generating plotly files')
        with open(path,'w') as f:
            f.write(title_md)
            f.write(update_date_md)
            f.write(body_md)
            f.write(javascript_md)
            f.write('*An error occurred in generating plots*')
        f.close()

if __name__ == '__main__':
    df=pd.read_csv('/home/pi/net_speed/log.txt',sep=';',index_col='Date')
    df.index=pd.to_datetime(df.index)
    write_markup(df)
    subprocess.call(['/home/pi/net_speed/pusher_of_page.sh'],shell=True)
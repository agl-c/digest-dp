from cgi import print_arguments
import pandas as pd

df = pd.read_csv("./data/wifi_on_ice.csv", nrows=50000)
data_o = df.to_numpy()
n = len(data_o)

data = []
for i in range(n):
    value = data_o[i][0].split(';')[-1]
    if(value == ''):
        continue
    # if(int(value)>1500):
    #     print("replace one sample with extrmely large value as 1500")
    #     data.append(1500)
    #     continue
    data.append(int(value))

tot = len(data)
print(tot)
df = pd.DataFrame(data, columns=['link_ping'])
# print(df)
df.to_csv("./data/49733rows_link_ping.csv")

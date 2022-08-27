from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict
# Include the `fusioncharts.py` file that contains functions to embed the charts.

from .fusioncharts import FusionCharts
import pandas as pd


# Pandas function to get the csv value
path = "/Users/nickytan/Documents/FS_Data_Science/FusionChartsProject/fusioncharts/utilities/company_list_state_classified.csv"
path2 = "/Users/nickytan/Documents/FS_Data_Science/FusionChartsProject/fusioncharts/utilities/df_companies_state.csv"
df = pd.read_csv(path, index_col=None)

df_companies_state = df.groupby("company_state").agg(
    total_companies=("company_state", "count")).reset_index()

df_companies_state = df_companies_state.sort_values(
    by=['total_companies'], ascending=False)


# Pandas function to modify csv value to generate map data
## For mapn chart
df_companies_state_id = pd.read_csv(path2, index_col=None)


df_companies_state_id["id"] = df_companies_state_id["id"].apply(lambda x : "00" + str(x) if x < 10 else "0" + str(x))
df_companies_state_id["total_companies"] = df_companies_state_id["total_companies"].apply(lambda x : str(x))
df_companies_state_id["value_label"] = "1"

x = [id for id in df_companies_state_id["id"]]
x2 =  [value for value in df_companies_state_id["total_companies"]]
x3 = [value for value in df_companies_state_id["value_label"]]

mapArray = list(map(list,zip(x,x2,x3)))


def myFirstChart(request):

    # Chart 1
    dataSource = OrderedDict()
    chartConfig = OrderedDict()

    chartConfig["caption"] = "Malaysia's state with total companies"
    chartConfig["subCaption"] = "Source from Jobstreet"
    chartConfig["xAxisName"] = "State"
    chartConfig["yAxisName"] = "Companies"

    chartConfig["theme"] = "fusion"

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    for state, value in zip(df_companies_state["company_state"], df_companies_state["total_companies"]):
        dataSource["data"].append({"label": state, "value": value})

    # Chart 2
    dataSourceMap = OrderedDict()

    mapConfig = OrderedDict()
    mapConfig["animation"] = "0"
    mapConfig["usehovercolor"] = "1"
    mapConfig["showlegend"] = "1"
    mapConfig["legendposition"] = "BOTTOM"
    mapConfig["legendborderalpha"] = "0"
    mapConfig["legendbordercolor"] = "#ffffff"
    mapConfig["legendallowdrag"] = "0"
    mapConfig["legendshadow"] = "0"
    mapConfig["caption"] = "Malaysia's state with total companies"
    mapConfig["subCaption"] = "Source from Jobstreet"
    mapConfig["connectorcolor"] = "000000"
    mapConfig["fillalpha"] = "80"
    mapConfig["hovercolor"] = "CCCCCC"
    mapConfig["theme"] = "fusion"

    colorDataObj = {
        "minvalue": "0",
        "code": "#FFE0B2",
        "gradient": "1",
        "color": [{
            "minValue": "0",
            "maxValue": "1000",
            "code": "#6497b1"
        }, {
            "minValue": "1000",
            "maxValue": "2000",
            "code": "#005b96"
        }, {
            "minValue": "2000",
            "maxValue": "3000",
            "code": "#03396c"
        }, {
            "minValue": "3000",
            "maxValue": "4000",
            "code": "#011f4b"
        }
        ]
    }

    dataSourceMap["chart"] = mapConfig
    dataSourceMap["colorrange"] = colorDataObj
    dataSourceMap["data"] = []

# Map data array
    mapDataArray = mapArray

    for i in range(len(mapDataArray)):
      dataSourceMap["data"].append({
          "id": mapDataArray[i][0],
          "value": mapDataArray[i][1],
          "showLabel": mapDataArray[i][2]
      })


    column2D = FusionCharts("column2d", "myFirstChart", "900",
                            "600", "myFirstchart-container", "json", dataSource)
    fusionMap = FusionCharts("maps/malaysia", "myFirstMap", "900", "600", "mySecondchart-container", "json", dataSourceMap)

    return render(request, 'index.html', {
        'output': column2D.render(),
        'output2': fusionMap.render()
})

defineVirtualDevice("DataAnalyzeModule", {
  title: "DataAnalyzeModule",
  cells: {
    "Temp1Status": {
    type: "value",
    value: false,
    readonly: false
    },
    "Temp2Status": {
    type: "value",
    value: false,
    readonly: false
    },
    "ThermoHeaterStatus": {
    type: "value",
    value: false,
    readonly: false
    },
    "LeakSensorStatus": {
    type: "value",
    value: false,
    readonly: false
    },
    "WaterLeakSenNormTime": {
    type: "value",
    value: 0,
    readonly: false
    },
    "TempSenNormTime": {
    type: "value",
    value: 0,
    readonly: false
    },
    "ThermoHeatNormTime": {
    type: "value",
    value: 0,
    readonly: false
    },
    "OutletsGlobalState": {
    type: "switch",
    value: false,
    readonly: false
    },
    "LightGlobalState": {
    type: "switch",
    value: false,
    readonly: false
    },
    "LeakSensorLastTime (minutes)": {
    type: "value",
    value: 0,
    readonly: false
    },
    "Temp1SensorLastTime (minutes)": {
    type: "value",
    value: 0,
    readonly: false
    },
    "Temp2SensorLastTime (minutes)": {
    type: "value",
    value: 0,
    readonly: false
    },
    "ThermoHeaterLastTime (minutes)": {
    type: "value",
    value: 0,
    readonly: false
    },
    "TemperatureGlobaErrorlFlag": {
    type: "switch",
    value: false,
    readonly: false
    },
    "WaterGlobaErrorlFlag": {
    type: "switch",
    value: false,
    readonly: false
    },
    "Temp1BatteryStatus": {
    type: "switch",
    value: false,
    readonly: false
    },
    "Temp2BatteryStatus": {
    type: "switch",
    value: false,
    readonly: false
    },
    "ThermoHeaterBatteryStatus": {
    type: "switch",
    value: false,
    readonly: false
    },
    "WaterBatteryStatus": {
    type: "switch",
    value: false,
    readonly: false
    },
    
  }
});
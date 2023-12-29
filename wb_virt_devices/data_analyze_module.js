defineVirtualDevice("DataAnalyzeModule", {
  title: "DataAnalyzeModule",
  cells: {
    "LeakSensorTimeError": {
    type: "switch",
    value: false,
    readonly: false
    },
    "Temp1SensorTimeError": {
    type: "switch",
    value: false,
    readonly: false
    },
    "Temp2SensorTimeError": {
    type: "switch",
    value: false,
    readonly: false
    },
    "ThermoHeaterTimeError": {
    type: "switch",
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
    "TempRegulator1Status": {
    type: "value",
    value: 0,
    readonly: false
    },
    "TempRegulator2Status": {
    type: "value",
    value: 0,
    readonly: false
    },
    "TempRegulator3Status": {
    type: "value",
    value: 0,
    readonly: false
    },
    "TempRegulator4Status": {
    type: "value",
    value: 0,
    readonly: false
    },
  }
});
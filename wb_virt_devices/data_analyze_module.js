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
      "OutletsGlobalState": {
      type: "switch",
      value: false,
      readonly: false
      },
      "LightGlobalState": {
      type: "switch",
      value: false,
      readonly: false
      }
    }
  });
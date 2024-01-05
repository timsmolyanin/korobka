defineVirtualDevice("SystemModule", {
  title: "SystemModule",
  cells: {
    "WiFi State": {
    type: "value",
    value: 0,
    readonly: false
    },
    "WiFi Client SSID": {
    type: "text",
    value: "",
    readonly: false
    },
    "WiFi Client Password": {
    type: "text",
    value: "",
    readonly: false
    },
    "ETH Mode": {
    type: "text",
    value: 0,
    readonly: false
    },
    "ETH IP": {
    type: "text",
    value: "",
    readonly: false
    },
    "ETH Mask": {
    type: "text",
    value: "",
    readonly: false
    },
    "ETH Gateway": {
    type: "text",
    value: "",
    readonly: false
    }
  }
});
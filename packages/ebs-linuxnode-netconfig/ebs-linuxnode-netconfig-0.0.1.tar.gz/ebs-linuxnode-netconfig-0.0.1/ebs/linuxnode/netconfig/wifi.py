

from typing import List
from pydantic import Field
from pydantic import BaseModel
from fastapi import Depends
from wpasupplicantconf import WpaSupplicantConf
from ebs.linuxnode.netconfig.core import app
from ebs.linuxnode.netconfig.core import auth_token

WPA_SUPPLICANT_PATH = '/home/chintal/wpa_supplicant.conf'


class WiFiScanProxy(object):
    pass


class WifiNetworkModel(BaseModel):
    ssid: str = Field(None, title="Wifi SSID")
    psk: str = Field(None, title="Wifi PSK (WPA2)")


class WPASupplicantProxy(object):
    def __init__(self, cpath='/etc/wpa_supplicant/wpa_supplicant.conf'):
        self._cpath = cpath
        self._config = self._read_config()

    def _read_config(self):
        with open(self._cpath, 'r') as f:
            lines = f.readlines()
            return WpaSupplicantConf(lines)

    def _write_config(self):
        with open(self._cpath, 'w') as f:
            self._config.write(f)

    def show_networks(self):
        networks = self._config.networks()
        return [WifiNetworkModel(ssid=k, psk=v['psk'])
                for k, v in networks.items()]

    def add_network(self, ssid, psk, **kwargs):
        self._config.add_network(ssid, psk=psk, key_mgmt="WPA-PSK", **kwargs)
        self._write_config()

    def remove_network(self, ssid):
        self._config.remove_network(ssid)
        self._write_config()


_wpa_supplicant = WPASupplicantProxy(WPA_SUPPLICANT_PATH)


class ActionResultModel(BaseModel):
    result: bool


@app.get("/wifi/networks/show", response_model=List[WifiNetworkModel], status_code=200)
async def show_configured_wifi_networks(token: str = Depends(auth_token)):
    return _wpa_supplicant.show_networks()


@app.post("/wifi/networks/add", response_model=ActionResultModel, status_code=201)
async def add_wifi_network(network: WifiNetworkModel, token: str = Depends(auth_token)):
    _wpa_supplicant.add_network(ssid=network.ssid, psk=network.psk)
    return {"result": True}


@app.post("/wifi/networks/remove", response_model=ActionResultModel, status_code=200)
async def remove_wifi_network(ssid: str, token: str = Depends(auth_token)):
    _wpa_supplicant.remove_network(ssid=ssid)
    return {"result": True}


@app.get("/wifi/status")
async def wifi_network_status(token: str = Depends(auth_token)):
    return {"message": "WNS"}


@app.get("/wifi/scan")
async def scan_wifi_networks(token: str = Depends(auth_token)):
    return {"message": "SN"}

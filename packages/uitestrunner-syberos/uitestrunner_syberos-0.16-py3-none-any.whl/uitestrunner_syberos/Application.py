from time import sleep
from . import Item
from lxml import etree


class Application:
    sopId = ""
    uiAppId = ""
    device = None

    def __init__(self, d=None, sop="", ui=""):
        self.sopId = sop
        self.uiAppId = ui
        self.device = d

    def launch(self, timeout=None):
        self.device.con.get(path="launchApp", args="sopid=" + self.sopId + "&" + "uiappid=" + self.uiAppId)
        if timeout is None:
            timeout = self.device.default_timeout
        for m_iter in range(0, timeout):
            self.device.refresh_layout()
            selector = etree.XML(self.device.xmlStr.encode('utf-8'))
            if selector.get("sopId") == self.sopId:
                return True
            sleep(1)
        return False

    def is_topmost(self):
        self.device.refresh_layout()
        selector = etree.XML(self.device.xmlStr.encode('utf-8'))
        if selector.get("sopId") == self.sopId:
            return True
        return False

    def close(self):
        self.device.con.get(path="quitApp", args="sopid=" + self.sopId)

    def __get_device_default_time(self):
        return self.device.default_timeout

    def find_item_by_xpath_key(self, xpath_key, timeout=None):
        return self.find_item_by_xpath(self.device.get_xpath(self.sopId, xpath_key), timeout)

    def find_item_by_xpath(self, xpath, timeout=None):
        if timeout is None:
            timeout = self.device.default_timeout
        for m_iter in range(0, timeout):
            if m_iter > 0:
                sleep(1)
            self.device.refresh_layout()
            selector = etree.XML(self.device.xmlStr.encode('utf-8'))
            nodes = selector.xpath(xpath)
            if selector.get("sopId") == self.sopId:
                if len(nodes) > 0:
                    node = nodes[0]
                    i = Item.Item(d=self.device, a=self, node=node, xpath=xpath)
                    return i
            else:
                raise Exception('error: application is not the top window!')
        raise Exception('timeout: not found that item!')

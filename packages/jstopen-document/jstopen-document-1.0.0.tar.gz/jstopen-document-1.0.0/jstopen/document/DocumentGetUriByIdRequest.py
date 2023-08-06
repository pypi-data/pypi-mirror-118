# -*- coding: utf-8 -*-

class DocumentGetUriByIdRequest():
    """根据id获取临时下载地址"""
    def __init__(self):
        """文件id"""
        self.id = None
        """临时地址过期时间（秒）"""
        self.expirySeconds = None
        self.usePrivate = False
        self.downloadLimitEnabled = True
        self.verifyCode = None
        self.verifyCodeEncodeType = None
        self.verifyCodeEnabled = None
        self.style = None
        self.watermark = None

    def getApiMethod(self):
        return 'document/getUriById'


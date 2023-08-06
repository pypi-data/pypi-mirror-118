# -*- coding: utf-8 -*-

class DocumentGetUriForUploadRequest():
    """获取文件临时上传地址"""
    def __init__(self):
        self.accessConfigName = 'default'
        self.accessObjectName = None
        self.expirySeconds = None
        self.usePrivate = False

    def getApiMethod(self):
        return 'document/getUriForUpload'

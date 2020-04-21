from mycelery.main import app
from mycelery.sms.yuntongxun.sms import CCP
from rentanapi.settings import constants

import logging

log = logging.getLogger("django")

@app.task(name="send_sms")
def send_sms(mobile, sms_code, sms_time):
    import time
    time.sleep(10)
    ccp = CCP()
    ret = ccp.send_template_sms(mobile, [sms_code, sms_time // 60], constants.SMS_TEMPLATE_ID)
    if ret == -1:
        log.error("发送短信失败！接受短信用户:%s" % mobile )
        return {"message": "短信发送失败！请刷新页面重新尝试发送或联系客服工作人员！"}
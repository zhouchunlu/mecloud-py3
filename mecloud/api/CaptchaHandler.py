# -*- coding: utf-8 -*-
from io import BytesIO


# TODO: 需要添加验证码缓存的定时清空
import tornado

from mecloud.api.BaseHandler import BaseHandler
from mecloud.helper.CaptchaHelper import CaptchaHelper
from mecloud.model.MeError import ERR_SUCCESS, ERR_AUTH_CAPTCHA


class CaptchaHandler(BaseHandler):
    stampCaptch = {}

    def get(self, stamp):
        captchaHelper = CaptchaHelper();
        code_img, capacha_code = captchaHelper.createCodeImage();
        CaptchaHandler.stampCaptch[stamp] = capacha_code

        msstream = BytesIO()
        code_img.save(msstream, "jpeg")
        code_img.close()
        self.set_header('Content-Type', 'image/jpg')
        tornado.web.RequestHandler.write(self,msstream.getvalue())

    def post(self, action):
        stamp = self.get_argument('stamp', None)
        captcha = self.get_argument('captcha', None)
        res = CaptchaHandler.freshCheck(stamp, captcha)
        if action == 'sms' and res:
            pass
        elif res:
            self.write(ERR_SUCCESS)
        else:
            self.write(ERR_AUTH_CAPTCHA)

    # 检查完后清空
    @staticmethod
    def freshCheck(stamp, captch):
        if stamp in CaptchaHandler.stampCaptch and (CaptchaHandler.stampCaptch[stamp] == captch):
            del (CaptchaHandler.stampCaptch[stamp])
            return True;
        elif stamp in CaptchaHandler.stampCaptch:
            del (CaptchaHandler.stampCaptch[stamp])
        return False;

    # 检查
    @staticmethod
    def check(stamp, captch):
        return CaptchaHandler.stampCaptch[stamp] == captch;

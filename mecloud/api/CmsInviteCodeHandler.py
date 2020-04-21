# coding=utf8
import copy
import traceback

import tornado.web
from mecloud.api.BaseHandler import BaseHandler
from mecloud.lib import InviteCodeUtil
from mecloud.model.MeError import ERR_SUCCESS, ERR_PARA
from mecloud.model.MeObject import MeObject


class CmsInviteCodeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, action=None):
        try:
            if action == 'createInviteCode':
                self.createInviteCode()
            else:
                print('action error ', action)
        except Exception as e:
            msg = traceback.format_exc()
            self.write(ERR_PARA.message)

    def post(self, action=None):
        pass

    def createInviteCode(self):
        count = int(self.get_argument('count', 1))
        if count > 100:
            count = 100
        i = 0
        list = []
        while (True):
            try:
                invite_code = MeObject('InviteCode')
                invite_code['code'] = InviteCodeUtil.create_code()
                invite_code['status'] = 0
                invite_code.save()
                list.append(invite_code['code'])
                i = i + 1
                if i >= count:
                    break
            except Exception as e:
                print(e)
        print('all finish')
        result = copy.deepcopy(ERR_SUCCESS.message)
        result['list'] = list
        self.write(result)

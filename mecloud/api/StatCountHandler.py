# -*- coding: utf-8 -*-

import json
import tornado.web
from copy import deepcopy

from mecloud.api.BaseHandler import BaseHandler
from mecloud.api.CountHandler import get_follow_ount
from mecloud.helper.Util import MeEncoder
from mecloud.lib import log
from mecloud.model.MeError import ERR_SUCCESS, ERR_USER_NOTFOUND


class StatCountHandler(BaseHandler):
    ### 获取对象 及 批量查询
    @tornado.web.authenticated
    def get(self):
        userId = self.get_current_user()
        if not userId:
            log.err( "get stat count error, from user not exist!" )
            self.write( ERR_USER_NOTFOUND.message )
            return

        otherUserId = None
        if 'otherUserId' in self.request.arguments:
            otherUserId = self.get_argument('otherUserId')

        is_mine = True
        if otherUserId and otherUserId != userId:
            is_mine = False

        if not is_mine:
            userId = otherUserId

        isUser = True
        if 'isUser' in self.request.arguments:
            if int(self.get_argument('isUser'))==0:
                isUser = False

        cia = get_follow_ount(userId, isUser)

        successInfo = deepcopy(ERR_SUCCESS)
        successInfo.message["data"] = cia
        self.write(json.dumps(successInfo.message, cls=MeEncoder))
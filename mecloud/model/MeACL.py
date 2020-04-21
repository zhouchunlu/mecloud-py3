# -*- coding: utf-8 -*-
'''
 * file :	MeACL.py
 * author :	bushaofeng
 * create :	2016-06-18 22:24
 * func : 
 * history:
'''
from mecloud.helper.ClassHelper import ClassHelper
from mecloud.model.DevelopUser import DevelopUser
from mecloud.model.MeRole import MeRole
from mecloud.model.MeUser import MeUser


class MeACL(dict):
    def __init__(self, acl=None):
        if acl == None:
            self['*'] = {'read': True, 'write': True}
        else:
            if not (isinstance(acl, dict)):
                raise TypeError('acl must a dict')
            for k in acl:
                self[k] = acl[k]

    ### 设置公共读权限
    def setPublicReadAccess(self, auth=True):
        if "*" not in self:
            self['*'] = {}
        self['*']['read'] = auth

    ### 设置公共写权限
    def setPublicWriteAccess(self, auth=True):
        if "*" not in self:
            self['*'] = {}
        self['*']['write'] = auth

    ### 设置角色读权限
    def setRoleReadAccess(self, role, auth=True):
        if not isinstance(role, MeRole):
            raise TypeError('role must a MeRole')
        if 'role:' + role['name'] not in self:
            self['role:' + role['name']] = {}
        self['role:' + role['name']]['read'] = auth

    ### 设置角色写权限
    def setRoleWriteAccess(self, role, auth=True):
        if not isinstance(role, MeRole):
            raise TypeError('role must a MeRole')
        if 'role:' + role['name'] not in self:
            self['role:' + role['name']] = {}
        self['role:' + role['name']]['write'] = auth

    ### 设置用户读权限
    def setUserReadAccess(self, user, auth=True):
        if not (isinstance(user, DevelopUser) or isinstance(user, MeUser)):
            raise TypeError('user must a MeUser')
        if user.objectId == None:
            raise TypeError('user must has saved')
        if user.objectId not in self:
            self[user.objectId] = {}
        self[user.objectId]['read'] = auth

    ### 设置用户写权限
    def setUserWriteAccess(self, user, auth=True):
        if not (isinstance(user, DevelopUser) or isinstance(user, MeUser)):
            raise TypeError('user must a MeUser')
        if user.objectId == None:
            raise TypeError('user must has saved')
        if user.objectId not in self:
            self[user.objectId] = {}
        self[user.objectId]['write'] = auth

    ### 获取用户是否有读权限
    def readAccess(self, user):
        if '*' in self and 'read' in self['*'] and self['*']['read']:
            return True
        # 如果user不为*，那么必须有为MeUser
        # if not (type(user) is MeUser):
        #    return False

        # 如果明确指定了某个用户的权限，则不再检查Role
        if user.objectId in self and 'read' in self[user.objectId] and self[user.objectId]['read']:
            return True
        # 检查role

        for k in self:
            if k.startswith('role:'):
                roleQuery = ClassHelper('Role')
                role = roleQuery.find_one({'name': k[5:], 'user': user.objectId})
                # 如果有一个角色有读权限，那么就有读权限
                if role is not None and 'read' in self[k] and self[k]['read']:
                    return True
        return False

    ### 获取用户是否有写权限
    def writeAccess(self, user):
        if '*' in self and 'write' in self['*'] and self['*']['write']:
            return True
        # 如果user不为*，那么必须有为MeUser
        # if not (type(user) is MeUser):
        #    return False

        # 如果明确指定了某个用户的权限，则不再检查Role
        if user.objectId in self and 'write' in self[user.objectId] and self[user.objectId]['write']:
            return True
        # 检查role
        for k in self:
            if k.startswith('role:'):
                roleQuery = ClassHelper('Role')
                role = roleQuery.find_one({'name': k[5:], 'user': user.objectId})
                # 如果有一个角色有读权限，那么就有读权限
                if role is not None and 'write' in self[k] and self[k]['write']:
                    return True
        return False


    ### 获取用户是否有删除权限
    def deleteAccess(self, user):
        # if self.has_key('*') and self['*'].has_key('delete') and self['*']['delete']:
        #     return True

        # 如果明确指定了某个用户的权限，则不再检查Role
        if user.objectId in self and 'delete' in self[user.objectId] and self[user.objectId]['delete']:
            return True
        # # 检查role
        # for k in self:
        #     if k.startswith('role:'):
        #         roleQuery = ClassHelper('Role')
        #         role = roleQuery.find_one({'name': k[5:], 'user': user.objectId})
        #         # 如果有一个角色有读权限，那么就有读权限
        #         if role is not None and self[k].has_key('delete') and self[k]['delete']:
        #             return True
        return False


    ### 更新超级用户权限
    def updateSuperAccess(self):
        if "*" not in self:
            self['*'] = {'read': True, 'write': True}
        wirteAcc = True
        readAcc = True
        for k in self:
            if k == '*':
                pass
            else:
                if 'write' in self[k] and self[k]['write']:
                    wirteAcc = False
                if 'read' in self[k] and self[k]['read']:
                    readAcc = False

        if not wirteAcc and not readAcc:
            del self['*']
        else:
            if not wirteAcc and 'write' in self["*"]:
                del self['*']['write']
            if not readAcc and 'write' in self["*"]:
                del self['*']['read']
        return self

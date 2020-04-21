#-*- coding: utf-8 -*- 
'''
 * file :	MeUser.py
 * author :	bushaofeng
 * create :	2016-06-09 17:37
 * func : 
 * history:
'''
import copy

from mecloud.helper.ClassHelper import ClassHelper
from mecloud.model.MeObject import MeObject


class MeUser(MeObject):
	def __init__(self, obj=None):
		MeObject.__init__(self, 'User', obj)

	def login(self, username, password):
		userHelper = ClassHelper(self.className)
		user = userHelper.find_one({'username': username, 'password': password})
		if user!=None:
			self.copySelf(user)
			del(user['username'])
			del(user['password'])
			return True
		else:
			return False

	### 注册
	def signup(self, username=None, password=None):
		self.save()

	### 修改密码
	def modPwd(self, username, password, newPwd):
		pass

	def loginWithoutPwd(self):
		appUserHelper = ClassHelper('develop', "AppUser")
		appUser = appUserHelper.find_one({'username': self['username']})
		obj = copy.deepcopy(self.dirty)
		if appUser==None:
			# 涉及到不同的应用，所以AppUser不存储bundleId和package
			if 'bundleId' in obj:
				del(obj['bundleId'])
			elif 'package' in obj:
				del(obj['package'])
			appUser = MeObject('develop', 'AppUser', obj)
			appUser.save()
		# 如果用户发生系统更新
		else:
			appUser = MeObject('develop', 'AppUser', appUser)
			if obj['system']!=appUser['system']:
				appUser['system'] = obj['system']
				appUser.save()

		userHelper = ClassHelper(self.appDb, 'User')
		user = userHelper.find_one({'username': obj['username']})
		if user==None or ('appUserId' not in user):
			self['appUserId'] = appUser.objectId
			self.save()
		else:
			self.copySelf(user)
			self.dirty.clear()
	
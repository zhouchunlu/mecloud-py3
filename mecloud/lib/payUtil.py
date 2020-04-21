# coding=utf-8

# 支付完成的回调
from mecloud.helper.ClassHelper import ClassHelper
from mecloud.lib import log


def orderCallback(oId, userId, status, order):
    '''
    根据支付结果更新订单的状态
    :param oId:RechargeFlow Id
    :param userId:用户Id
    :param status: 支付是否成功，1为成功，3为等待验证
    :param order:第三方平台返回订单信息，包括错误码
    :return:
    '''
    log.debug('oId:%s, userId:%s, status:%d, order:%s', oId, userId, status, order)
    ###更新充值流水记录
    orderHelper = ClassHelper("RechargeFlow")
    rechargeFlow = orderHelper.get(oId)
    walletHelper = ClassHelper("Wallet")
    walletInfo = walletHelper.find_one({"user": userId})
    if status == 1:  # 充值成功,更新钱包
        rechargeFlow_action = {'destClass': 'RechargeFlow',
                               'query': {"_id": oId},
                               'action': {"@set": {"status": status, "order": order}}}
        if not walletInfo:  # 未找到钱包直接创建
            wallet = {"user": userId, 'balance': rechargeFlow['amount']}
            walletInfo = walletHelper.create(wallet, transaction=[rechargeFlow_action])
        else:
            wallet = {
                "$inc": {'balance': rechargeFlow['amount']}
            }
            walletInfo = walletHelper.update(walletInfo['_id'], wallet, transaction=[rechargeFlow_action])
            return walletInfo
    else:
        rechargeFlow = orderHelper.update(oId, {"$set": {"status": status, "order": order}})
        return rechargeFlow



# def orderCallback(oId, userId, status, order):
#     log.debug('oId:%s, userId:%s, status:%d, order:%s', oId, userId, status, order)
#     '''
#     根据支付结果更新订单的状态
#     :param oId:RechargeFlow Id
#     :param userId:用户Id
#     :param status: 支付是否成功，1为成功，0为失败
#     :param order:第三方平台返回订单信息，包括错误码
#     :return:
#     '''
#     item = {
#         "$set": {
#             "status": status,
#             "order": order
#         }
#     }
#     ###更新充值流水记录
#     orderHelper = ClassHelper("RechargeFlow")
#     rechargeFlow = orderHelper.update(oId, item)
#     if rechargeFlow and status == 1:
#         ###更新钱包
#         walletHelper = ClassHelper("Wallet")
#         walletInfo = walletHelper.find_one({"user": userId})
#         if walletInfo:
#             wallet = {
#                 "$inc": {'balance': rechargeFlow['amount']}
#             }
#             wallet = walletHelper.update(walletInfo['_id'], wallet)
#         else:
#             wallet = {"user": userId, 'balance': rechargeFlow['amount']}
#             walletHelper.create(wallet)
#         if wallet:
#             return wallet.update(rechargeFlow)
#         else:
#             return None
#     else:
#         return None

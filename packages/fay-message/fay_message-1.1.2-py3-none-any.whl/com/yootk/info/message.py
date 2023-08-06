#coding:UTF-8

url = 'www.yootk.com'  #自定义属性

_url = 'www.yootk.com'

def get_message():
#    print('message.get_message(): __name__ = %s' % __name__) #com.yootk.info.message  模块名称
    return 'get_message(): www.yootk.com'
    
def echo_message(msg):
    return 'echo_message(): %s' % msg
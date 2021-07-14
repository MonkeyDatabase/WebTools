from pocbase import POCBase


class DemoPOC(POCBase):
    vulID = '1571'                  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1'                   # 默认为1
    author = 'seebug'               # PoC作者的大名
    vulDate = '2014-10-16'          # 漏洞公开的时间,不知道就写今天
    createDate = '2014-10-16'       # 编写 PoC 的日期
    updateDate = '2014-10-16'       # PoC 更新的时间,默认和编写时间一样
    references = ['https://xxx.xx.com.cn']      # 漏洞地址来源,0day不用写
    name = 'XXXX SQL注入漏洞 PoC'   # PoC 名称
    appPowerLink = 'https://www.drupal.org/'    # 漏洞厂商主页地址
    appName = 'Drupal'          # 漏洞应用名称
    appVersion = '7.x'          # 漏洞影响版本

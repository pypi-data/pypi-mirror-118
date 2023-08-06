import os
import sys
import time
import curses
import random
import curses
import cursor
import requests
import threading
import ctypes
import configparser
import json
import zipfile
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from requests.models import ContentDecodingError
from sys import *
_black=1
_red=2
_green=3
_yellow=4
_blue=5
_magenta=6
_cyan=7
_white=8
_grey=9
black=_black
red=_red
green=_green
yellow=_yellow
blue=_blue
magenta=_magenta
cyan=_cyan
white=_white
grey=_grey
_version='N0Lib:0.0.2'
__N0Version__=''
__SETVERSION__=False
__DEBUG__=False 
__GRAPHIC__=False
__dirChar__='/'  
__WORKPATH__='./'
__SHELLPATH__='./'
__FLITERMODE__='half'
__COLORFLITER__='$n0p'
__COLORFLITERS__={'c3h7n3o9':[161,209,215,84,88,40,34,58],
'rainbow':[161,209,215,192,84,88,82,40,28,56],
'fak3':[483,484,485,486,487,488],
'mengd@':[47,52,100,40,202],
't0ki':[141,148,184,178,219,220],
'metal':[236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254],
'chalk':[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
'bbc':[149,119,156,115,114],
'secret':[0,1,1,1,0,1],
'void':[1]}
__MAILSETTINGS__={
    'host':'$n0p',
    'user':'$n0p',
    'password':'$n0p',
    'sender':'$n0p'
}
__PublicVarPool__={'LASTRET':'$n0p'}
class LOG:
    x=0
    y=0
    hight=0
    lenth=0
    total=0#总日志行数 [!]:非显示行数
    showEndLine=0#显示日志总行数
    limitCol=0
    limitLine=0
    color=_white
    showFlag=False
    path=''
    boarderX='-'
    boarderY='|'
    logName='Log'
    rawOutputLog=list()
    rawColor=list()
    showOutputLog=list()
    showColor=list()
    def __init__(self,_x,_y,_lenth=20,_hight=7,_boarderX='-',_boarderY='|',_color=_white,_path='./'):
        self.x=_x
        self.y=_y
        self.hight=_hight
        self.lenth=_lenth
        self.limitCol=_lenth-2
        self.limitLine=_hight-2
        self.path=_path
        self.showEndLine=0#初始化后showEndLine在0行
        self.color=_color
        self.boarderX=_boarderX
        self.boarderY=_boarderY
        self.rawOutputLog=list()#不在init里重新赋值的话两个LOG对象的变量会被python分配同一个地址
        self.rawColor=list()
        self.showOutputLog=list()
        self.showColor=list()
    def out(self,_string):
        self.rawOutputLog.append(str(_string))
    def output(self,_string,colorStr='$n0p'): 
        global __GRAPHIC__
        _string=str(_string)
        if not __GRAPHIC__:
            print(_string.replace('\n',' '))
            return
        if _string=='':
            self.show()
            return
        #OUTPUT('[in out put]')
        if colorStr=='$n0p':
            colorStr=str(len(_string))+'|grey'
        def delColor(__colorStr):
            rubbish,leftColorSt=divide(__colorStr,',')
            return leftColorSt
        def addColor(__colorStr,__colorLenth,__colorWhat):
            if __colorStr=='$n0p':
                __colorStr=str(__colorLenth)+'|'+__colorWhat
            else:
                __colorStr+=','+str(__colorLenth)+'|'+__colorWhat
            return __colorStr
        
        self.rawOutputLog.append(str(_string))#原始日志数据
        self.rawColor.append(str(colorStr))#原始颜色信息
        right=_string.replace('\n',' ')
        lines=0
        lineLengths=list()
        while True:#切分过长字符串
            if realLength(right)>self.limitCol:
                left,right=_divideStrByRealLength(right,self.limitCol)
                #OUTPUT(left+'<numberDividerReturn>'+right)缩到左侧=self.limitCol
                lineLengths.append(len(left))
                self.showOutputLog.append(left)
            else:
                if right!='':
                    self.showOutputLog.append(right)
                    lineLengths.append(len(right))
                    lines+=1
                #OUTPUT('try out while')
                break
            #OUTPUT(left+'<outputWileTrue>'+right)
            lines+=1
        self.showEndLine+=lines#向下移动显示结束行
        #OUTPUT('showEndLine:'+str(self.showEndLine))
        leftColorStr=colorStr
        index=0
        while lines>0:#储存颜色
            lineLeft=lineLengths[index]
            #lineLeft=self.limitCol
            newColorStr='$n0p'
            while lineLeft>0:
                if leftColorStr!='$n0p':#有颜色可用
                    colors=listDivider(leftColorStr,',')#每行取出剩余的颜色
                    #OUTPUT('leftColorStr into colors:'+str(colors))
                    leftColorStr='$n0p'#取出后置空
                    for color in colors:
                        useColorLenth=0#本行当前颜色使用量
                        colorLenth,colorWhat=divide(color,'|')
                        colorLenth=beNumber(colorLenth)
                        if colorLenth<=0:
                                #leftColorStr=delColor(leftColorStr)#删掉一个颜色
                                continue#如果当前颜色用尽则换下一个
                        if lineLeft>0:
                            if colorLenth>=lineLeft:#当前颜色超过本行
                                useColorLenth=lineLeft
                                colorLenth-=lineLeft#当前颜色剩余
                                leftColorStr=addColor(leftColorStr,colorLenth,colorWhat)#没用完当写入leftColorStr
                                lineLeft=0
                            else:#当前颜色不足本行
                                useColorLenth=colorLenth
                                lineLeft-=colorLenth
                            newColorStr=addColor(newColorStr,useColorLenth,colorWhat)#使用了颜色
                        else:
                            leftColorStr=addColor(leftColorStr,colorLenth,colorWhat)#未使用颜色直接写入leftColorStr
                        #OUTPUT('leftColorStr:'+str(leftColorStr))
                    #colors[index]=newColorStr#把填充后的颜色代码写回去
                else:#无颜色部分默认灰色
                    newColorStr=addColor(newColorStr,lineLeft,'grey')
                    lineLeft=0
            lines-=1
            index+=1
            self.showColor.append(newColorStr)
        self.total+=1
        #OUTPUT('showOutputLog:'+str(self.showOutputLog))
        #OUTPUT('showColor:'+str(self.showColor))
        self.show()
    def clear(self):
        for i in range(0,self.hight-2):
            drawLine(self.x+1,self.y+i+1,' ',self.lenth-1,self.color)
    def change(self,_x,_y,_lenth,_hight):
        self.x=_x
        self.y=_y
        self.hight=_hight
        self.lenth=_lenth
        self.limitCol=_lenth-2
        self.limitLine=_hight-2
    def draw(self,drawColor=-1):
        if drawColor==-1:
            drawColor=self.color
        drawLine(self.x,self.y,self.boarderX,self.lenth,drawColor)
        drawLine(self.x,self.y+self.hight-1,self.boarderX,self.lenth,drawColor)
        verticalLine(self.x,self.y,self.boarderY,self.hight,drawColor)
        verticalLine(self.x+self.lenth,self.y,self.boarderY,self.hight,drawColor)
    def show(self,endLine=-1):
        if not __GRAPHIC__:
            return
        def strColor2intColor(strColor):
            try:
                return eval('_'+strColor)
            except:
                try:
                    return int(strColor)
                except:
                    return _grey
        if endLine==-1:
            endLine=self.showEndLine
        if endLine<self.limitLine:
            startLine=0
        else:
            startLine=endLine-self.limitLine
        #OUTPUT('startLine:'+str(startLine)+'|'+str(endLine))
        self.clear()
        outIndex=0
        for lineId in range(startLine,endLine):
            #OUTPUT('lineId:'+str(lineId))
            showColors=listDivider(self.showColor[lineId],',')#每行输出前取出该行颜色指导字符串并切割
            showPoint=0#重置输出指针
            for color in showColors:
                colorLenth,colorWhat=divide(color,'|')#切分出作用域和颜色
                colorLenth=beNumber(colorLenth)
                say(self.x+1+showPoint,self.y+1+outIndex,self.showOutputLog[lineId][showPoint:showPoint+colorLenth],strColor2intColor(colorWhat))#输出
                showPoint+=colorLenth#输出指针后移
            outIndex+=1
    def drop(self):
        self.total=0
        self.showEndLine=0
        self.rawOutputLog=list()
        self.rawColor=list()
        self.showOutputLog=list()
        self.showColor=list()
    def setSize(self,_length=20,_hight=7):
        self.hight=_hight
        self.lenth=_length
        self.limitCol=_length-2
        self.limitLine=_hight-2
    def scroll(self):
        nowEndLine=self.showEndLine
        drawColor=229
        drawLine(self.x,self.y,'-',self.lenth,drawColor)
        drawLine(self.x,self.y+self.hight-1,'-',self.lenth,drawColor)
        verticalLine(self.x,self.y,'}',self.hight,drawColor)
        verticalLine(self.x+self.lenth,self.y,'{',self.hight,drawColor)
        while True:
            _press=consoleWin.getch()
            if _press==ord('q'):
                break
            elif _press ==curses.KEY_UP:#上滚
                nowEndLine-=1
                if nowEndLine<self.limitLine:#请求显示的区域小于显示区域最后一行
                    nowEndLine+=1
                else:
                    self.show(nowEndLine)
            elif _press==curses.KEY_DOWN:#下滚
                nowEndLine+=1
                if nowEndLine>self.showEndLine:#请求显示的区域大于有记录的最后一行
                    nowEndLine-=1
                else:
                    self.show(nowEndLine)
        self.draw()
    def save(self):
        global __N0Version__
        if __N0Version__!='':
            retVer=_version+'\\'+__N0Version__
        else:
            retVer=_version
        outContent='### N0Lib '+retVer+' Output Log ###\n'+str(time.asctime( time.localtime(time.time())))+'\n---[0]---\n'
        index=1
        for item in self.rawOutputLog:
            outContent+=item+'\n---['+str(index)+']---\n'
            index+=1
        createFile(self.path+self.logName,outContent)
def N0HELP(_function='$n0p'):
    WHO={
        'N0P3':'Developed by N0P3. Thank you. http://n0p3.cn',
        'T0KI':'Hey!',
        'MENGD@':'Hello! N0Lib. http://men9da.cn',
        'C3H7N3O9':'Where is my seal?'
        }
    HELPS={
        'version':'查看Lib版本',
        'setVersion':'打包自己的N0Lib版本。(版本名)',
        'initGraphic':'先初始化图形模式才可以使用涉及位置颜色的函数。',
        'endGraphic':'将终端恢复。',
        'safeExit':'能将程序妥善退出的函数。用它来代替exit(0)吧！',
        'consoleOut':'向默认存在的OutputWin(默认输出窗口)输出。(输出者,输出内容,[输出者颜色],[内容颜色],[染色字符串],[是否受滤镜影响]) 当染色字符串存在时，内容颜色将不起作用。输出者颜色有两个特殊值，"SPACE","TAB"，前者会隐藏输出者，后者会将输出者的位置置空。',
        'debugOut':'与consoleOut完全一致的用法，除了它仅在DEBUG模式下才执行，以及一定不受滤镜影响。',
        'rainbowOut':'非常多彩的consoleOut。(输出者,输出内容,[输出者颜色],[循环颜色序列],[循环开始颜色],[循环结束颜色],[是否输出],[是否受滤镜影响]) 参数会造成什么影响自己实验一下吧(doge; 如果把输出关闭，rainbowOut也可以作为生成多彩染色字符串的工具。',
        'echo':'简单输出。(字符串,[颜色]) 在你打算将某程序改用N0Lib开发的版本时，可以将print简单替换为echo。也许偶尔简单的输出一下很方便，不过还是更建议使用consoleOut。',
        'flowSay':'紧跟在上一次SAY的后面输出。(字符串,[颜色])',
        'SAY':'在屏幕任意位置输出字符串。(输出横坐标,输出纵坐标,字符串,[颜色],[是否打印背景],[背景字符])',
        'realLength':'获取字符串显示长度。(字符串)',
        'verticalLine':'绘制竖线。(输出横坐标,输出纵坐标,打印字符,[颜色])',
        'drawLine':'绘制横线。(输出横坐标,输出纵坐标,打印字符,[颜色])',
        'openFile':'打开文件。(文件路径)',
        'beNumber':'把字符串数字转为整型数字。(字符串数字)',
        'download':'下载文件。(链接,[保存文件名])',
        'publicVar':'查改增公开变量。(变量名,[值]) 当值为空时为获取变量的值。',
        'divider':'按字符切割字符串。(字符串,切割字符) 把字符串按第一次出现的字符切成两半。',
        'listDivider':'把字符串按字符切段。(字符串,切割字符) 返回list',
        'stringCompare':'忽略大小写判断两字符串是否相等。(字符串1,字符串2)',
        'splitPath':'切分路径。（路径) 依次返回文件名和剩余路径',
        'sniper':"精确取出某标签内容。(标签列表,页面文本) 例如：sniper(['head','div','p'],web)将取出第一个head标签内的第一个div标签的第一个p标签内容。如果想要选取并列的其他同名标签,请在标签名后加<x>,x为第几个重名标签。例如:sniper(['head','div<2>','p<3>'],web)将取出第一个head标签内的第二个div标签的第三个p标签内容。",
        'tapExtarctor':'从页面中取出第一次出现的指定标签内容。(标签名,页面文本,[标签参数字符串])',
        'legalPath':'把路径转为合法路径。(路径) 试一试。',
        'realPath':'把路径转为真实路径。(路径,[是否为文件]) ',
        'randomString':'生成随机字符串。(生成长度)',
        'request':'请求页面。(请求方法,url,[get参数(dict)],[post参数(dict),[headers(dict)],[timeout],[是否以流模式传输]) 基于requests封装的请求函数。方法有get,post,json。json模式会自动将post参数转为json格式，并在请求头中声明数据格式为json。',
        'createFile':'创建文件。(目标文件路径,文件内容,[重复文件重命名]) 如果路径中的文件夹不存在将会创建。如果文件已经存在默认会给文件名+1并创建，此功能可以通过createIndex=False关闭。关闭后文件存在将返回$n0p。文件创建成功返回OK,覆盖返回COVER',
        'createJsonFile':'创建json文件。(目标文件路径,字典(dict),[重复文件重命名]) 如果路径中的文件夹不存在将会创建。如果文件已经存在默认会给文件名+1并创建，此功能可以通过createIndex=False关闭。关闭后文件存在将返回$n0p。文件创建成功返回OK,覆盖返回COVER',
        'flagExtractor':'从文本中取出所有符合格式的flag。(文本,flag格式) flag格式例如：flag{},n0p3{} 记得带上一对花括号。',
        'patchDict':"为一个字典进行补充。(字典,patch字典) 例如: dict1={'a':1,'b':2,'c':3} dict2={'a':4,'d':5} patch(dict1,dict2)将返回一个新字典 {'a': 4, 'b': 2, 'c': 3, 'd': 5} ",
        'N0HELP':'为开发者提供帮助。(函数名)',
        'N0DEBUG':'启用或关闭DEBUG模式。(开关(bool))',
        'getWidth':'获取一个字符的字节数。(字符)',
        'zipDir':'把一个文件夹压缩成zip。(文件夹路径,压缩后文件名)',
        'unzip':'解压zip。(zip文件路径,解压路径)',
        'nargv':'从命令行获取参数。',
        'setFliter':'设置滤镜。(滤镜名,[滤镜模式]) 模式默认为half，不会对输出者造成影响，改为all将对所有consoleOut结果造成影响。',
        'addFliter':'添加新的滤镜。(滤镜名,颜色列表)',
        'newArgv':'将命令行参数向前偏移。(开始保留的参数序号) 某些情况下会用到。',
    }
    if _function !='$n0p':
        if _function.upper() in WHO:
            consoleOut(_function,WHO[_function.upper()],_yellow,_cyan)
        elif _function in HELPS:
            consoleOut(_function,HELPS[_function],119,_white)
        else:
            echo("No command '"+_function -+"'.",_red)
    else:
        _viewDict(OutputWin,HELPS)
        consoleOut('LOG','日志类非常有用，所有的输出都可以交给它。',_blue,_white)
        consoleOut('LOG','change(x,y,length,hight)修改窗口左上角坐标，长度和高度','TAB',_yellow)
        consoleOut('LOG','draw(color)画出边框，参数是颜色','TAB',_yellow)
        consoleOut('OutputWin','OutputWin是默认的LOG类')
def version():
    global __N0Version__
    if __N0Version__!='':
        retVer=_version+'\\'+__N0Version__
    else:
        retVer=_version
    echo(retVer)
def setVersion(versionName):
    global __N0Version__,__SETVERSION__
    if not __SETVERSION__:
        __N0Version__=versionName
        __SETVERSION__=True
def realLength(target):
    length=0
    for i in target:
        length+=getWidth(i)
    return length
def _divideStrByRealLength(string,targetLength):
    real_length=0
    retStr=''
    index=0
    for i in string:
        index+=1
        real_length+=getWidth(i)
        retStr+=i
        if real_length>=targetLength:
            return retStr,string[index:]
    return '>>RETURN<<LINEHEAD>>FAILED<<','>>RETURN<<LINEHEAD>>FAILED<<'
def verticalLine(_x,_y,TheChar,length,fColor=_grey):
    for i in range(0,length):
        say(_x,_y+i,TheChar,fColor)
def _viewDict(_window,_dict=dict()):
    for _key in _dict:
        _window.output(_key+':'+_dict[_key],str(len(_key)+1)+'|119,'+str(len(_dict[_key]))+'|white')
def drawLine(_x,_y,TheChar,length,fColor=_grey):
    say(_x,_y,TheChar*length,fColor)
def openFile(fileName):
    if fileName!='$n0p':
        try:
            file=open(fileName,"r+")
        except:
            consoleOut('+',"ERROR[005]: '"+fileName+"' not found.")
            return '$n0p'
        return file
    else:
        return '$n0p'
def say(x,y,word,fColor=_white,clear=False,clearChar=' '):
    if __GRAPHIC__:
        if clear:
            clearChar=clearChar[0]
            say(x,y,clearChar*realLength(word))
        global __OUTX__,__OUTY__
        word=str(word)
        if x<=__limitX__ and y<=__limitY__ and x>0 and y>0:
            x=x-1
            y=y-1
            try: 
                fColor=int(fColor)
                consoleWin.addstr(y,x,word,_setColor(fColor))
                __OUTX__=x+1+len(word)
                __OUTY__=y+1
            except: 
                consoleOut('Old out','SAY excuted error.')
        else:
            consoleOut('Old out','[SAY]: Error posite.<'+str(x)+','+str(y)+'>')
        consoleWin.refresh()
    else:
        if __DEBUG__:
            print('[SAY]:ERROR! Please use initGraphic().')
def _setColor(fontColor,backColor=-1):
    return curses.color_pair(fontColor)
def flowSay(word,fColor=_white):
    say(__OUTX__,__OUTY__,word,fColor)
def echo(content,color=_white,**kv):
    consoleOut('[Egg_002]:How can you see me!',content,'SPACE',color,COLORFLITER=True)
def beNumber(ToBeNumber):
    try:
        ToBeNumber=int(ToBeNumber)
        return ToBeNumber
    except:
        say(1,1,'Error:'+str(ToBeNumber)+' is not a legal number.',_red)
        return '$n0p'
def sizeFormat(size, isDisk=False, precision=2):
    formats = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    unit = 1000.0 if isDisk else 1024.0
    if not(isinstance(size, float) or isinstance(size, int)):
        consoleOut('sizeFormat','Not number.')
    if size < 0:
        raise ValueError('number must be non-negative')
    for i in formats:
        size /= unit
        if size < unit:
            return f'{round(size, precision)}{i}'
    return f'{round(size, precision)}{i}'
def download(url,fileName='$n0p'):
    size=0
    chunk_size=1024
    if fileName=='$n0p':
        fileName,rubbish=splitPath(url)
    web=request('get',url,_stream=True)
    if web!='$n0p':
        if web.status_code==200:
            try:
                content_size=web.headers['content-length']
                with open(__SHELLPATH__+fileName,'wb') as code:
                    for data in web.iter_content(chunk_size = chunk_size):
                        code.write(data)
                        size+=len(data)
                        download_info='Download ['+fileName+']: '+str(sizeFormat(float(size)))+'/'+str(sizeFormat(float(content_size)))
                        drawLine(OutputWin.x+1,OutputWin.y+OutputWin.hight-1,' ',realLength(download_info),OutputWin.color)
                        say(OutputWin.x+1,OutputWin.y+OutputWin.hight-1,download_info,OutputWin.color)
                consoleOut('download','Success.',_yellow,_green)
            except Exception as e:
                consoleOut('download','FAILED.'+str(e),_red,_red)
        else:
            consoleOut('download','Failed. <'+str(web.status_code)+'>',_red,_red)
    else:
        consoleOut('download','Connect failed.',_red,_white)
    OutputWin.draw()
def publicVar(publicVarName,_value='$n0p'):
    publicVarName=publicVarName.replace('$','')
    publicVarName=publicVarName.replace('(','')
    publicVarName=publicVarName.replace(')','')
    if _value=='$n0p':
        try:
            _value=__PublicVarPool__[publicVarName]
            return _value
        except:
            debugOut("ERROR","<008> Get $("+publicVarName+") failed.",rightColor=_white)
            return '$n0p'
    else:
        try:
            __PublicVarPool__[publicVarName]=str(_value)
        except:
            debugOut('publicVarSync',"$("+publicVarName+") synchronizes failed.")
def divide(string,TheChar,delESC=False):
    RIGHT=False
    right=""
    left=""
    string=str(string)
    for i in range(len(string)):
        char=string[i]
        if char ==TheChar and (not RIGHT) and string[i-1]!='\\':
            RIGHT=True
        else:
            if not RIGHT:
                left+=char
            else:
                right+=char
    if delESC:
        left=left.replace('\\','')
        right=right.replace('\\','')
    if not RIGHT:
        return left,'$n0p'
    else:
        return left,right
def listDivider(strTargetList,TheChar):
    retList=list()
    leftOne,rightOne=divide(strTargetList,TheChar)
    retList.append(leftOne)
    while rightOne!='$n0p'and rightOne!='':
        leftOne,rightOne=divide(rightOne,TheChar)
        retList.append(leftOne)
    return retList
def stringCompare(str1,str2):
    str1=str1.lower()
    str2=str2.lower()
    if str1==str2:
        return True
    else:
        return False
def splitPath(_path):
    items=listDivider(_path,__dirChar__)
    #consoleOut('splitePath',items)
    fileName=items.pop()
    retPath=''
    #items.reverse()
    for i in items:
        retPath+=i+__dirChar__
    return fileName,retPath
def esc(targetStr,escList='$n0p'):
    if escList=='$n0p':
        specialChar=['$','(',')','*','+','.','[',']','?','^','\\','{','}','|']
    else:
        specialChar=escList
    targetStr=list(targetStr)
    index=0
    SKIP=False
    for char in targetStr:
        if not SKIP:
            if char in specialChar:
                targetStr.insert(index,'\\')
                SKIP=True
        else:
            SKIP=False
        index+=1
    retStr=''
    for i in targetStr:
        retStr+=i
    #debugOut('ESC',retStr)
    return retStr
def sendEmail(receivers,subject,content,sender='$n0p',mailHost='$n0p',mailUser='$n0p',mailPass='$n0p',SELF=True):
    if sender=='$n0p':
        sender=__MAILSETTINGS__['sender']
    if mailHost=='$n0p':
        mailHost=__MAILSETTINGS__['host']
    if mailUser=='$n0p':
        mailUser=__MAILSETTINGS__['user']
    if mailPass=='$n0p':
        mailPass=__MAILSETTINGS__['password']
    if '$n0p' in [sender,mailHost,mailUser,mailPass]:
        consoleOut('Send Email','Mail-Sender not set.',117,_red)
        return '$n0p'
    receivers=receivers.split(',')
    if SELF:
        receivers.append(sender)
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mailHost, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mailUser, mailPass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        debugOut('Send Email','Mail has been send successfully.',117)
        return 'OK'
    except smtplib.SMTPException as e:
        debugOut('Send Email','Mail send failed! '+str(e),117,_red)
        return '$n0p'
    except Exception as e:
        debugOut('Send Email','Mail send failed! '+str(e),117,_red)
        return '$n0p'

def match(left,right,targetStr,onlyContent=True):
    matchLeft=esc(left)#正则特殊字符加反斜杠
    matchRight=esc(right)
    debugOut('MATCH','Try to match '+left+'...'+right,LEVEL=2)
    flags=[]
    while True:
        reFlag=re.search(matchLeft+".+?"+matchRight,targetStr)
        try:
            findFlag=reFlag.group(0)
            if onlyContent:
                flags.append(findFlag[len(left):0-len(right)])
            else:
                flags.append(findFlag)
            targetStr=targetStr.replace(findFlag,'',1)
        except:
            debugOut("match","Match finished.")
            break
    return flags

def sniper(_tagList,_web):
    content=_web
    for i in _tagList:
        content=_web
        i,right=divide(i,'<')
        if right!='$n0p':
            #consoleOut(i,'Target:'+right[:-1])
            targetNum=int(right[:-1])
        else:
            targetNum=1
        index=0
        while True:
            debugOut('TryMatch',content,_cyan,_white)
            find=tagExtractor(i,content)
            index+=1
            if index==targetNum:
                content=find
                break
            else:
                content=content.replace('<'+i+'>'+find+'</'+i+'>','',1)
        debugOut(i,content,_cyan,_white)
    return content
def tagExtractor(tagName,targetStr,tagParamStr='',unknowParam=False):
    #targetStr=targetStr.replace('\\','')#去掉python自动添加的反斜杠
    #consoleOut('Old out','\n\n'+targetStr+'\n\n')
    import re
    if tagName=='!--':#注释
        try:
            dataStart=re.search("<!--",targetStr).start()+4
            dataEnd=re.search("-->",targetStr).start()
            return targetStr[dataStart+1:dataEnd]
        except:
            return "$n0p"
    else:
        tagName=esc(tagName)#正则特殊字符加反斜杠
        tagParamStr=esc(tagParamStr)
        if tagParamStr!='':
            _tagParamStr=' '+tagParamStr
        else:
            _tagParamStr=tagParamStr
        debugOut('tagExtractor','Try to match <'+tagName+_tagParamStr+'>...</'+tagName+'>')
        try:
            rawStr=targetStr
            if not unknowParam:
                dataStart=re.search("<"+tagName+_tagParamStr+">",targetStr).start()+len(tagName+_tagParamStr)+1
            else:
                dataStart=re.search("<"+tagName+_tagParamStr,targetStr).start()+len(tagName+_tagParamStr)+1
            dataEnd=0
            before=0
            while True:
                dataEnd=re.search("</"+tagName+">",targetStr).start()
                dataEnd=before+dataEnd
                if dataEnd<dataStart+1:
                    #targetStr=targetStr[:dataEnd]+n0pstr(len(tagName)+3)+targetStr[dataEnd+len(tagName)+3:]
                    targetStr=targetStr[dataStart+1:]
                    before=dataStart+1
                    #print(targetStr)
                else:
                    break
            return rawStr[dataStart+1:dataEnd]
        except Exception as e:
            return '$n0p'
def legalPath(_path):
    if _path!='':
        if _path[-1]!=__dirChar__:
            _path+=__dirChar__
        _path=_path.replace('N0:/',__WORKPATH__)#N0目录转linux目录
        if len(_path)>2:
            _path=_path[:2]+_path[2:].replace('./','')#去当前目录
    return _path
def realPath(_path,isFile=False):
    retPath=legalPath(_path)
    if retPath=='$n0p/':#当前shell目录
        targetPath=__SHELLPATH__
    elif retPath[0]=='/':#绝对路径
        targetPath=retPath
    else:#相对路径
        targetPath=__SHELLPATH__+retPath
    if isFile:
        return targetPath[:-1]
    else:
        return targetPath
def randomString(_length):
    randomStr = ''
    baseStr = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(baseStr) - 1
    for i in range(_length):
        randomStr += baseStr[random.randint(0, length)]
    return randomStr
def request(_method,targetURL,paramsData='$n0p',postData='$n0p',_header='$n0p',_timeout=3,_stream=False):
    if paramsData=='$n0p':
        paramsData=list()
    if postData=='$n0p':
        postData=list()
    if _header=='$n0p':
        _header={'User-Agent':"N0P3's N0Lib."}
    if _timeout!='$n0p':
        _timeout=beNumber(_timeout)
    else:
        _timeout=2
    if _method=='get':
        try:
            ret=requests.get(targetURL,params=paramsData,headers=_header,timeout=_timeout,stream=_stream)
            return ret
        except:
            debugOut("requestsGET","Connect failed.")
            return '$n0p'
    elif _method=='post':
        try:
            ret=requests.post(targetURL,data=postData,params=paramsData,headers=_header,timeout=_timeout,stream=_stream)
            return ret
        except:
            debugOut("requestsPOST","Connect failed.")
            return '$n0p'
    elif _method=='json':    
        _header=patchDict(_header,{"Content-Type":"application/json;charset=UTF-8"})
        try:
            ret=requests.post(targetURL,headers=_header,data=json.dumps(postData),params=paramsData,timeout=_timeout,stream=_stream)
            return ret
        except:
            debugOut("requestsJSON","Connect failed.")
            return '$n0p'
    else:
        return '$n0p'
def createFile(filePath,content,createIndex=True,overwrite=False):
    _dirs=listDivider(filePath,__dirChar__)#分出路径
    _fileName=_dirs.pop()
    _path=''
    index=0
    indexChar=''
    for item in _dirs:
        _path +=item+__dirChar__#每个循环路径进一级
        if not os.path.isdir(_path):  # 无文件夹时创建
            os.makedirs(_path)
    _file=os.path.splitext(_fileName)
    _fileName=_file[0]
    suffix=_file[-1]
    while True:
        #consoleOut('Old out',_path+_fileName)
        if not os.path.isfile(_path+_fileName+indexChar+suffix):  # 无文件时创建
            fd = open(_path+_fileName+indexChar+suffix, mode="w", encoding="utf-8")
            fd.write(content)
            fd.close()
            debugOut('Create file',_path+_fileName+indexChar+suffix)
            return 'OK'
        else:#文件已存在
            if createIndex:
                index+=1
                indexChar=str(index)
            else:
                if overwrite:
                    fd = open(_path+_fileName+indexChar+suffix, mode="w", encoding="utf-8")
                    fd.write(content)
                    fd.close()
                    debugOut('Overwrite',_path+_fileName+indexChar+suffix)
                    return 'OK'
                else:
                    return '$n0p'
def createJsonFile(filePath, content_dict, createIndex = True):
    #创建一个json文件。
    dirs = listDivider(filePath, '/')#分出路径
    fileName,suffix = divide(dirs.pop(), '.')
    if suffix != '$n0p':
        suffix = '.'+suffix
    else:
        suffix = ''
    path = ''
    index = 0
    indexChar = ''
    for item in dirs:
        path  += item+'/'#每个循环路径进一级
        if not os.path.isdir(path):  # 无文件夹时创建
            os.makedirs(path)
    while True:
        #consoleOut('Old out',path+fileName)
        if not os.path.isfile(path+fileName+indexChar+suffix):  # 无文件时创建
            fd  =  open(path+fileName+indexChar+suffix, mode = "w", encoding = "utf-8")
            fd.write(json.dumps(content_dict))
            fd.close()
            #debugOut('Create file',path+fileName+indexChar)
            debugOut('createJsonFile', path+fileName+indexChar+suffix+' success.')
            return 'OK'
        else:#文件已存在
            if createIndex:
                index += 1
                indexChar = str(index)
            else:
                fd  =  open(path+fileName+indexChar+suffix, mode = "w", encoding = "utf-8")
                fd.write(json.dumps(content_dict))
                fd.close()
                #debugOut('Create file',path+fileName+indexChar)
                debugOut('createJsonFile', 'Cover '+path+fileName+indexChar+suffix+' success.')
                return 'OK'
        #-----
def flagExtractor(string,_flagFormat):
    flags=[]
    _flagFormat=_flagFormat.replace('{}','')
    while True:
        reFlag=re.search(_flagFormat+"{.+?}",string)
        try:
            findFlag=reFlag.group(0)
            flags.append(findFlag)
            string=string.replace(findFlag,'')
        except:
            debugOut("flagExtractor","Flags search finished.")
            break
    return flags
def patchDict(_oldDict,_patch):
    #更新dict中已有的，新增没有的.无法删除.
    for item in _patch:
        _oldDict[item]=_patch[item]
    return _oldDict
def rainbowOut(identity,content,leftColor=_grey,colorList=[161,209,215,84,88,40,34,58],colorStart=-1,colorEnd=-1,output=True,COLORFLITER=True):
    retColorStr='0|grey'
    colorIndex=0
    try:
        colorList=__COLORFLITERS__[colorList]
    except:
        pass
    if colorStart>=0 and colorEnd>=0:
        colorList=[]
        if colorStart<colorEnd:
            for i in range(colorStart,colorEnd):
                colorList.append(i)
        else:
            for i in range(colorEnd,colorStart):
                colorList.append(i)
                colorList.reverse()
        for i in range(colorStart,colorEnd):
            colorList.append(i)
    SKIP=False
    lenth=len(content)
    Loop=True
    while Loop:
        if colorList==[]:
            retColorStr=str(lenth)+'|grey'
            Loop=False
        elif len(colorList)==1:
            retColorStr=str(lenth)+'|'+str(colorList[0])
            Loop=False
        else:
            for color in colorList:
                if SKIP:
                    SKIP=False
                    continue
                else:
                    if colorIndex<=lenth:
                        retColorStr+=',1|'+str(color)
                        colorIndex+=1
                    else:
                        Loop=False
                        break
        colorList.reverse()
        SKIP=True
    if output:
        consoleOut(identity,content,leftColor,colorStr=retColorStr,COLORFLITER=COLORFLITER)
    return retColorStr
def debugOut(identity,_content,leftColor='grey',rightColor='grey',colorStr='$n0p'):
    if __DEBUG__:
        consoleOut(identity,_content,leftColor,rightColor,colorStr,False)#debug信息不受影响
def consoleOut(identity,_content,leftColor='grey',rightColor='grey',colorStr='$n0p',COLORFLITER=True):
    identity=str(identity)
    _content=str(_content)
    leftColor=str(leftColor)
    rightColor=str(rightColor)
    TAB=False
    SPACE=False
    if leftColor=='TAB':
        leftColor='grey'
        TAB=True
    elif leftColor=='SPACE':
        leftColor='grey'
        SPACE=True
    def identityColor(identity):
        if not SPACE and __FLITERMODE__!='all' or not COLORFLITER:
            if identity=='WARNING':
                colorStr='10|yellow,'
            elif identity=='ERROR':
                colorStr='8|red,'
            elif identity=='OK':
                colorStr='5|green,'
            elif identity=='TIP':
                colorStr='6|cyan,'
            elif identity=='+' or identity=='C':
                colorStr='4|white,'
            else:
                colorStr=str(len(identity)+4)+'|'+leftColor+','
        else:
            colorStr=''
        return colorStr
    if __COLORFLITER__!='$n0p' and COLORFLITER:
        try:
            if __FLITERMODE__=='all':
                #如果滤镜模式是all的话，rainbowOut生成的颜色还需要算上len(identity)+4个字符
                colorStr=rainbowOut(identity,identity+'N0P3'+_content,leftColor,__COLORFLITERS__[__COLORFLITER__],output=False)
            else:
                colorStr=rainbowOut(identity,_content,leftColor,__COLORFLITERS__[__COLORFLITER__],output=False)
        except:
            pass
    if colorStr=='$n0p':#不启用颜色指导字符串
        #_colorStr=addColor(_colorStr,len(_content),'white')
        colorStr=identityColor(identity)
        colorStr+=str(len(_content)+1)+'|'+rightColor
    else:#启用
        _keepColorStr=colorStr
        colorStr=identityColor(identity)
        colorStr+=_keepColorStr
    if SPACE:
        OutputWin.output(_content,colorStr)
    elif TAB:
        OutputWin.output((len(identity)+4)*' '+_content,colorStr)
    else:
        OutputWin.output("["+identity+"]: "+_content,colorStr)
def N0DEBUG(_bool):
    global __DEBUG__
    if _bool==True:
        __DEBUG__=True
    else:
        __DEBUG__=False
def getWidth( char ):
    """Return the screen column width for unicode ordinal o."""
    o=ord(char)
    widths = [
    (126,  1), (159,  0), (687,   1), (710,  0), (711,  1),
    (727,  0), (733,  1), (879,   0), (1154, 1), (1161, 0),
    (4347,  1), (4447,  2), (7467,  1), (7521, 0), (8369, 1),
    (8426,  0), (9000,  1), (9002,  2), (11021, 1), (12350, 2),
    (12351, 1), (12438, 2), (12442,  0), (19893, 2), (19967, 1),
    (55203, 2), (63743, 1), (64106,  2), (65039, 1), (65059, 0),
    (65131, 2), (65279, 1), (65376,  2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
    ]
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if o <= num:
            return wid
    return 1
def zipDir(startdir,file_news):
    #文件夹路径,压缩包名字
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
        debugOut('zip','Success!',_green,_white)
    z.close()
def unzip(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    debugOut('zipsrc',zip_src)
    if r:     
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        debugOut('unzip','Success!',_green,_white)
        return 'OK'
    else:
        debugOut('zip','This is not a zip file.',_red,_white)
        return '$n0p'
def nargv(id):
    try:
        ret=argv[id]
    except:
        ret='$n0p'
    return ret
def setFliter(name,mode='half'):
    global __COLORFLITER__,__FLITERMODE__
    __COLORFLITER__=name
    __FLITERMODE__=mode
def addFliter(name,colorList):
    global __COLORFLITERS__
    __COLORFLITERS__[name]=colorList
def newArgv(offset):
    index=offset
    retParts=list()
    while True:
        ret=nargv(index)
        if ret!='$n0p':
            retParts.append(ret)
        else:
            return retParts
        index+=1
def initGraphic():
    global consoleWin,__limitX__,__limitY__,__GRAPHIC__
    if not __GRAPHIC__:
        consoleWin = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        cursor.hide()
        __limitY__=curses.LINES-1
        __limitX__=curses.COLS-1
        curses.noecho()
        curses.cbreak()
        consoleWin.keypad(True)
        __GRAPHIC__=True
    else:
        pass
def safeExit():
    endGraphic()
    sys.exit(0)
def endGraphic():
    global __GRAPHIC__
    if __GRAPHIC__:
        __GRAPHIC__=False
        curses.nocbreak()
        consoleWin.keypad(False)
        curses.echo()
        curses.endwin()
    cursor.show()

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 13:16:07 2017

@author: gason
"""

# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.split(__file__)[0],'script'))

import re
import time
import pandas as pd
import report as rpt

import warnings
warnings.filterwarnings("ignore")

mytemplate='template.pptx'

print('=='*15+'[reportgen 工具包]'+'=='*15)

#==================================================================
while 1:
    #print('=' * 70)
    try:
        command = input('''
==========一、数据导入=======
1.导入问卷星数据并编码.
2.导入问卷网数据并编码.
3.导入已编码好的数据.
请输入相应的序号:
''')
            
        if command in ['0','exit']:
            #print('开始下一步...')
            break
        if command=='1':
            print('准备导入问卷星数据，请确保“.\data\”文件夹下有按序号和按文本数据(如100_100_0.xls、100_100_2.xls).')
            filepath='.\\data'
            if os.path.isdir(filepath):
                filelist=os.listdir(filepath)
                wjx_data={}
                n1=n2=0
                for f in filelist:
                    s1=re.findall('(\d+_\d+)_0.xls',f)
                    s2=re.findall('(\d+_\d+)_2.xls',f)
                    if s1:
                        if s1[0] in wjx_data:
                            wjx_data[s1[0]][0]=f
                        else:
                            wjx_data[s1[0]]=[f,'']
                    if s2:
                        if s2[0] in wjx_data:
                            wjx_data[s2[0]][1]=f
                        else:
                            wjx_data[s2[0]]=['',f]
                tmp=[k for k in wjx_data if int(len(wjx_data[k][0])>0)+int(len(wjx_data[k][1])>0)==2]
                if len(tmp)==1:
                    # 刚好只识别出一组问卷星数据
                    filename1=os.path.join(filepath,tmp[0]+'_0.xls')
                    filename2=os.path.join(filepath,tmp[0]+'_2.xls')
                elif len(tmp)>1:
                    print('脚本识别出多组问卷星数据，请选择需要编码的数据：')
                    for i,k in enumerate(tmp):
                        print('{i}:  {k}'.format(i=i+1,k=k+'_0.xls/'+k+'_2.xls'))
                    ii=input('您选择的数据是(数据前的编码，如：1):')
                    if ii.isnumeric():
                        filename1=os.path.join(filepath,tmp[int(ii)-1]+'_0.xls')
                        filename2=os.path.join(filepath,tmp[int(ii)-1]+'_2.xls')
                    else:
                        print('您输入正确的编码.')
                        continue
                else:
                    print('在.\\data目录下没有找到任何的问卷星数据，请返回检查.')
                    continue          
            try:
                data,code=rpt.wenjuanxing([filename1,filename2])
                data,code=rpt.spec_rcode(data,code)
            except Exception as e:
                print(e)
                print('问卷星数据导入失败, 请检查.')
                continue
            cross_qlist=list(sorted(code,key=lambda c: int(re.findall('\d+',c)[0])))
            print('将题目进行编码......\n')
            for k in cross_qlist:
                print('{key}:  {c}'.format(key=k,c=code[k]['content']))
                time.sleep(0.1)
            rpt.save_code(code,'code.xlsx')
            rpt.save_data(data,'data.xlsx')
            rpt.save_data(data,'data_readable.xlsx',code)
            print('\n编码完毕, 编码后的数据已经保存在本地为data.xlsx和code.xlsx. \n')
            break
        if command=='2':
            print('准备导入问卷网数据，请确保“.\data\”文件夹下有按序号、按文本和code数据.')
            try:
                data,code=rpt.wenjuanwang()
            except Exception as e:
                print(e)
                print('问卷网数据导入失败, 请检查.')
                continue
            cross_qlist=list(sorted(code,key=lambda c: int(re.findall('\d+',c)[0])))
            print('将题目进行编码......\n')
            for k in cross_qlist:
                print('{key}:  {c}'.format(key=k,c=code[k]['content']))
                time.sleep(0.1)
            rpt.save_code(code,'code.xlsx')
            rpt.save_data(data,'data.xlsx')
            rpt.save_data(data,'data_readable.xlsx',code)
            print('编码完毕, 编码后的数据已经保存在本地为data.xlsx和code.xlsx. \n')
            break               
        if command=='3':
            data_name=input('请输入数据的文件名，缺省为 data.xlsx. 请输入:')
            if not data_name:
                data_name='data.xlsx'
            try:
                data=rpt.read_data(data_name)
                print('已成功导入data.')
            except Exception as e:
                print(e)
                print('data导入失败, 请检查')
                continue
            code_name=input('请输入code的文件名，缺省为 code.xlsx. 请输入:')
            if not code_name:
                code_name='code.xlsx'
            try:
                code=rpt.read_code(code_name)
                print('已成功导入code.')
            except Exception as e:
                print(e)
                print('code导入失败, 请检查')
                continue
            cross_qlist=list(sorted(code,key=lambda c: int(re.findall('\d+',c)[0])))
            print('题目编码情况如下......\n')
            for k in cross_qlist:
                print('{key}:  {c}'.format(key=k,c=code[k]['content']))
                time.sleep(0.1)
            break
    except Exception as e:
        print(e)
        print('错误..')

os.system('pause')


s='''
==========二、数据预处理=======
1. 编码后的数据中，data.xlsx用于存放所有按序号数据，code.xlsx用于存放序号对应的文本内容以及报告生成所需变量

2. code中key[必须]：题号，content[必须]:题目内容，qtype[必须]:题目类型，qlist[必须]：题目在data.xlsx对应的位置，code_order:用于固定报告中选项的顺序,weight:用于求加权平均值，如NPS、满意度、模块满意度等.

3. 本脚本不提供数据处理操作，因为没有界面体验很不好.大家可以在本地处理好数据后，重新导入编码后并修改好的数据。在这个过程中，如果涉及到选项序号的合并、修改等，请同步修改data和code两个文件，谢谢.

4. 如果需要修改数据，可以输入exit或者quit暂时退出本脚本，等数据修改完后再启动.
--------------------------------
'''
print(s)
command=input('请输入(按任意键跳转到第三步：报告生成)：')

if command in ['0','exit','quit']:
    print('本工具包由JSong开发, 谢谢使用, 再见..')
    exit()


#=======================================================================
while 1:
    print('=' * 70)
    try:
        command = input('''
==========三、报告生成=======.
x. 全自动一键生成
1. 整体统计报告自动生成
2. 交叉分析报告自动生成
3. 描述统计
4. 交叉分析
5. 对应分析
0. 退出程序(也可以输入exit或者quit)
请输入相应的序号:
''')
        if command in ['x','X']:
            filename=input('请输入需要保存的文件名,缺省为 reportgen报告自动生成: ')
            if not filename:
                filename=u'reportgen报告自动生成'
            print('请耐心等待，脚本正在马不停蹄地工作中......')
            rpt.onekey_gen(data,code,filename=filename,template=mytemplate);
            print('\n 所有报告已生成, 请检查文件夹：'+os.path.join(os.getcwd(),'out'))
            print('\n 开始生成*scorpion.xlsx*,请耐心等待')
            try:
                rpt.scorpion(data,code)
            except :
                print('脚本出现一些错误...')
            continue
        if command in ['0','exit','quit']:
            print('本工具包由JSong开发, 谢谢使用, 再见..')
            break
        if command=='1':
            filename=input('请输入需要保存的文件名,缺省为调研报告初稿: ')
            if not filename:
                filename=u'调研报告初稿'
            rpt.summary_chart(data,code,filename=filename,template=mytemplate);
            print('\n 报告已生成: '+os.path.join(os.getcwd(),'out',filename+'.pptx'))
            continue
        if command=='2':
            qq=input('请输入需要交叉分析的变量(例如: Q1): ')
            qq=qq.upper()
            if qq in code:
                print('您输入的是%s: %s'%(qq,code[qq]['content']))
            else:
                print('没有找到您输入的题目,请返回重新输入.')
                continue
            if code[qq]['qtype'] not in ['单选题','多选题']:
                print('您选择的题目类型不是单选题或者多选题，本脚本暂时无法支持，请重新输入！')
                continue
            filename=qq+'_差异分析'
            save_dstyle=['FO','TGI','CHI']
            print('脚本正在努力生成报告中，请耐心等待........')
            try:
                rpt.cross_chart(data,code,qq,filename=filename,save_dstyle=save_dstyle,template=mytemplate);
                print('\n 报告已生成: '+os.path.join(os.getcwd(),'out',filename+'.pptx'))
            except Exception as e:
                print(e)
                print('报告生成过程出现错误，请重新检查数据和编码.')
                continue                  
        if command=='3':
            qq=input('请输入需要统计的变量(例如: Q1): ')
            qq=qq.upper()
            if qq in code:
                print('您输入的是%s: %s'%(qq,code[qq]['content']))
            else:
                print('没有找到您输入的题目,请返回重新输入.')
                continue
            if code[qq]['qtype'] not in ['单选题','多选题','排序题','矩阵单选题']:
                print('您选择的题目类型本脚本暂时无法支持，请重新输入！')
                continue
            try:
                t=rpt.qtable(data,code,qq)
                if not(t['fo'] is None):
                    print('百分比表如下：')
                    print(t['fop'])
                    print('--'*10)
                    print('频数表如下:')
                    print(t['fo'])
            except Exception as e:
                print(e)
                print('脚本运行错误，请重新检查数据和编码.')
                continue

        if command=='4':
            qq1=input('请输入需要交叉分析的行变量，也是因变量(例如: Q1): ')
            if qq1 in code:
                print('您输入的是%s: %s'%(qq1,code[qq1]['content']))
            else:
                print('没有找到您输入的题目,请返回重新输入.')
                continue
            qq2=input('请输入需要交叉分析的列变量，也是自变量(例如: Q1): ')
            if qq2 in code:
                print('您输入的是%s: %s'%(qq2,code[qq2]['content']))
            else:
                print('没有找到您输入的题目,请返回重新输入.')
                continue
            if code[qq2]['qtype'] not in ['单选题','多选题']:
                print('您选择的自变量题目类型不是单选题或者多选题，本脚本暂时无法支持，请重新输入！')
                continue
            try:
                t=rpt.qtable(data,code,qq1,qq2)
                if not(t['fo'] is None):
                    print('百分比表如下：')
                    print(t['fop'])
                    print('--'*10)
                    print('频数表如下:')
                    print(t['fo'])
            except Exception as e:
                print(e)
                print('脚本运行错误，请重新检查数据和编码.')
                continue
        if command=='5':
            qq1=input('请输入需要对应分析的行变量，也是因变量(例如: Q1): ')
            if qq1 in code:
                print('您输入的是%s: %s'%(qq1,code[qq1]['content']))
            else:
                print('没有找到您输入的题目,请返回重新输入.')
                continue
            qq2=input('请输入需要交叉分析的列变量，也是自变量(例如: Q1): ')
            if qq2 in code:
                print('您输入的是%s: %s'%(qq2,code[qq2]['content']))
            else:
                print('没有找到您输入的题目,请返回重新输入.')
                continue
            if code[qq2]['qtype'] not in ['单选题','多选题']:
                print('您选择的自变量题目类型不是单选题或者多选题，本脚本暂时无法支持，请重新输入！')
                continue
            try:
                t=rpt.qtable(data,code,qq1,qq2)['fo']
                x,y,inertia=rpt.mca(t)
                title=u'对应分析图(信息量为{:.1f}%)'.format(inertia[1]*100)
                fig=rpt.scatter([x,y],title=title)
                filename='ca_'+qq1+'_'+qq2
                fig.savefig(filename+'.png',dpi=1200)
                w=pd.ExcelWriter(filename+'.xlsx')
                x.to_excel(w,startrow=0,index_label=True)
                y.to_excel(w,startrow=len(x)+2,index_label=True)
                w.save()
                print('该对应分析能解释{:.1f}%的信息,相应的图片和数据已保存为：'.format(inertia[1]*100))
                print('图片： '+filename+'.png')
                print('数据(可利用PPT的散点图绘制更漂亮的图表)：'+filename+'.xlsx')
                try:
                    from PIL import Image
                    img=Image.open(filename+'.png')
                    img.show()
                except:
                    pass
            except Exception as e:
                print(e)
                print('脚本运行错误，请重新检查数据和编码.')
                continue
        os.system('pause')
    except Exception as e:
        print(e)
        print('错误..')
        

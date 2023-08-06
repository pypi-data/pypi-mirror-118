import time #line:1
import pandas as pd #line:3
class cleverminer :#line:5
    version_string ="0.0.82"#line:7
    def __init__ (O0OOO00O00O000OOO ,**OOOOOOOO0000000O0 ):#line:9
        O0OOO00O00O000OOO ._print_disclaimer ()#line:10
        O0OOO00O00O000OOO .stats ={'total_cnt':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:18
        O0OOO00O00O000OOO ._init_data ()#line:19
        O0OOO00O00O000OOO ._init_task ()#line:20
        if len (OOOOOOOO0000000O0 )>0 :#line:21
            O0OOO00O00O000OOO .kwargs =OOOOOOOO0000000O0 #line:22
            O0OOO00O00O000OOO ._calc_all (**OOOOOOOO0000000O0 )#line:23
    def _init_data (O0OO0OO0OO00OOO00 ):#line:25
        O0OO0OO0OO00OOO00 .data ={}#line:27
        O0OO0OO0OO00OOO00 .data ["varname"]=[]#line:28
        O0OO0OO0OO00OOO00 .data ["catnames"]=[]#line:29
        O0OO0OO0OO00OOO00 .data ["vtypes"]=[]#line:30
        O0OO0OO0OO00OOO00 .data ["dm"]=[]#line:31
        O0OO0OO0OO00OOO00 .data ["rows_count"]=int (0 )#line:32
        O0OO0OO0OO00OOO00 .data ["data_prepared"]=0 #line:33
    def _init_task (O000O0OO0OO0OOOOO ):#line:35
        O000O0OO0OO0OOOOO .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'traces':[],'generated_string':'','filter_value':int (0 )}#line:44
        O000O0OO0OO0OOOOO .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:48
        O000O0OO0OO0OOOOO .hypolist =[]#line:49
        O000O0OO0OO0OOOOO .stats ['total_cnt']=0 #line:51
        O000O0OO0OO0OOOOO .stats ['total_valid']=0 #line:52
        O000O0OO0OO0OOOOO .stats ['control_number']=0 #line:53
        O000O0OO0OO0OOOOO .result ={}#line:54
    def _get_ver (OOOOOO000OO000OO0 ):#line:56
        return OOOOOO000OO000OO0 .version_string #line:57
    def _print_disclaimer (O00000000000OOO00 ):#line:59
        print ("***********************************************************************************************************************************************************************")#line:60
        print ("Cleverminer version ",O00000000000OOO00 ._get_ver ())#line:61
        print ("IMPORTANT NOTE: this is preliminary development version of CleverMiner procedure. This procedure is under intensive development and early released for educational use,")#line:62
        print ("    so there is ABSOLUTELY no guarantee of results, possible gaps in functionality and no guarantee of keeping syntax and parameters as in current version.")#line:63
        print ("    (That means we need to tidy up and make proper design, input validation, documentation and instrumentation before launch)")#line:64
        print ("This version is for personal and educational use only.")#line:65
        print ("***********************************************************************************************************************************************************************")#line:66
    def _prep_data (OOO0O000OO00OO00O ,OO00OO0000O000OOO ):#line:68
        print ("Starting data preparation ...")#line:69
        OOO0O000OO00OO00O ._init_data ()#line:70
        OOO0O000OO00OO00O .stats ['start_prep_time']=time .time ()#line:71
        OOO0O000OO00OO00O .data ["rows_count"]=OO00OO0000O000OOO .shape [0 ]#line:72
        OOOO000OOOO0OOO00 =0 #line:73
        O000OOOOO0O0O0O00 =0 #line:74
        for O0O000OOOO0OOOO00 in OO00OO0000O000OOO :#line:75
            print ('Column: '+O0O000OOOO0OOOO00 )#line:77
            OOO0O000OO00OO00O .data ["varname"].append (O0O000OOOO0OOOO00 )#line:78
            OOOO0OOO0000O0OO0 =pd .get_dummies (OO00OO0000O000OOO [O0O000OOOO0OOOO00 ])#line:79
            O0OO000000O0OOO0O =0 #line:80
            if (OO00OO0000O000OOO .dtypes [O0O000OOOO0OOOO00 ].name =='category'):#line:81
                O0OO000000O0OOO0O =1 #line:82
            OOO0O000OO00OO00O .data ["vtypes"].append (O0OO000000O0OOO0O )#line:83
            OO0O0O0OOO0OOO000 =0 #line:86
            O00O00O000000OOOO =[]#line:87
            O00O000O0OOO000O0 =[]#line:88
            for O000O00O0000OOO0O in OOOO0OOO0000O0OO0 :#line:90
                print ('....category : '+str (O000O00O0000OOO0O )+" @ "+str (time .time ()))#line:92
                O00O00O000000OOOO .append (O000O00O0000OOO0O )#line:93
                OO000OO000O000O00 =int (0 )#line:94
                OOOO0OOO0O0OO00O0 =OOOO0OOO0000O0OO0 [O000O00O0000OOO0O ].values #line:95
                for OO00O00O000000000 in range (OOO0O000OO00OO00O .data ["rows_count"]):#line:97
                    if OOOO0OOO0O0OO00O0 [OO00O00O000000000 ]>0 :#line:98
                        OO000OO000O000O00 +=1 <<OO00O00O000000000 #line:99
                O00O000O0OOO000O0 .append (OO000OO000O000O00 )#line:100
                OO0O0O0OOO0OOO000 +=1 #line:110
                O000OOOOO0O0O0O00 +=1 #line:111
            OOO0O000OO00OO00O .data ["catnames"].append (O00O00O000000OOOO )#line:113
            OOO0O000OO00OO00O .data ["dm"].append (O00O000O0OOO000O0 )#line:114
        print (OOO0O000OO00OO00O .data ["varname"])#line:116
        print (OOO0O000OO00OO00O .data ["catnames"])#line:117
        print (OOO0O000OO00OO00O .data ["vtypes"])#line:118
        OOO0O000OO00OO00O .data ["data_prepared"]=1 #line:120
        print ("Data preparation finished ...")#line:121
        print ('Number of variables : '+str (len (OOO0O000OO00OO00O .data ["dm"])))#line:122
        print ('Total number of categories in all variables : '+str (O000OOOOO0O0O0O00 ))#line:123
        OOO0O000OO00OO00O .stats ['end_prep_time']=time .time ()#line:124
        print ('Time needed for data preparation : ',str (OOO0O000OO00OO00O .stats ['end_prep_time']-OOO0O000OO00OO00O .stats ['start_prep_time']))#line:125
    def bitcount (OO000OO0O0000O0OO ,O00O0OO000O0O0O00 ):#line:128
        OO000OO0O00O00OO0 =0 #line:129
        while O00O0OO000O0O0O00 >0 :#line:130
            if (O00O0OO000O0O0O00 &1 ==1 ):OO000OO0O00O00OO0 +=1 #line:131
            O00O0OO000O0O0O00 >>=1 #line:132
        return OO000OO0O00O00OO0 #line:133
    def _verifyCF (OO00O000OOOOOO00O ,_O0000OO0O0000O0O0 ):#line:136
        O0000O00OOO0O0OOO =bin (_O0000OO0O0000O0O0 ).count ("1")#line:137
        OOOOOO0O0O0OOOO00 =[]#line:138
        OO0OO0OO0OOOOO0OO =[]#line:139
        OOO0O00OOO0O0O0OO =0 #line:140
        OO00O00O0O00O0O00 =0 #line:141
        O0000000OOOO00OOO =0 #line:142
        O000000O000000000 =0 #line:143
        OO00O0O0OO000OO0O =0 #line:144
        OO000OOO000O00OO0 =0 #line:145
        O0000000O00OOO0O0 =0 #line:146
        OOO0OOO00OO0O0OOO =0 #line:147
        O0O00O0OOOOO0OO00 =0 #line:148
        O00OOO0O00OOOOOOO =OO00O000OOOOOO00O .data ["dm"][OO00O000OOOOOO00O .data ["varname"].index (OO00O000OOOOOO00O .kwargs .get ('target'))]#line:149
        for O00OOO0O0O0O0O0O0 in range (len (O00OOO0O00OOOOOOO )):#line:150
            OO00O00O0O00O0O00 =OOO0O00OOO0O0O0OO #line:151
            OOO0O00OOO0O0O0OO =bin (_O0000OO0O0000O0O0 &O00OOO0O00OOOOOOO [O00OOO0O0O0O0O0O0 ]).count ("1")#line:152
            OOOOOO0O0O0OOOO00 .append (OOO0O00OOO0O0O0OO )#line:153
            if O00OOO0O0O0O0O0O0 >0 :#line:154
                if (OOO0O00OOO0O0O0OO >OO00O00O0O00O0O00 ):#line:155
                    if (O0000000OOOO00OOO ==1 ):#line:156
                        OOO0OOO00OO0O0OOO +=1 #line:157
                    else :#line:158
                        OOO0OOO00OO0O0OOO =1 #line:159
                    if OOO0OOO00OO0O0OOO >O000000O000000000 :#line:160
                        O000000O000000000 =OOO0OOO00OO0O0OOO #line:161
                    O0000000OOOO00OOO =1 #line:162
                    OO000OOO000O00OO0 +=1 #line:163
                if (OOO0O00OOO0O0O0OO <OO00O00O0O00O0O00 ):#line:164
                    if (O0000000OOOO00OOO ==-1 ):#line:165
                        O0O00O0OOOOO0OO00 +=1 #line:166
                    else :#line:167
                        O0O00O0OOOOO0OO00 =1 #line:168
                    if O0O00O0OOOOO0OO00 >OO00O0O0OO000OO0O :#line:169
                        OO00O0O0OO000OO0O =O0O00O0OOOOO0OO00 #line:170
                    O0000000OOOO00OOO =-1 #line:171
                    O0000000O00OOO0O0 +=1 #line:172
                if (OOO0O00OOO0O0O0OO ==OO00O00O0O00O0O00 ):#line:173
                    O0000000OOOO00OOO =0 #line:174
                    O0O00O0OOOOO0OO00 =0 #line:175
                    OOO0OOO00OO0O0OOO =0 #line:176
        OOO00OOOOOO0O00OO =True #line:179
        for OOO0OO0O0OOO0O0OO in OO00O000OOOOOO00O .quantifiers .keys ():#line:180
            if OOO0OO0O0OOO0O0OO =='Base':#line:181
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=O0000O00OOO0O0OOO )#line:182
            if OOO0OO0O0OOO0O0OO =='RelBase':#line:183
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=O0000O00OOO0O0OOO *1.0 /OO00O000OOOOOO00O .data ["rows_count"])#line:184
            if OOO0OO0O0OOO0O0OO =='S_Up':#line:185
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=O000000O000000000 )#line:186
            if OOO0OO0O0OOO0O0OO =='S_Down':#line:187
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=OO00O0O0OO000OO0O )#line:188
            if OOO0OO0O0OOO0O0OO =='S_Any_Up':#line:189
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=O000000O000000000 )#line:190
            if OOO0OO0O0OOO0O0OO =='S_Any_Down':#line:191
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=OO00O0O0OO000OO0O )#line:192
            if OOO0OO0O0OOO0O0OO =='Max':#line:193
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=max (OOOOOO0O0O0OOOO00 ))#line:194
            if OOO0OO0O0OOO0O0OO =='Min':#line:195
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=min (OOOOOO0O0O0OOOO00 ))#line:196
            if OOO0OO0O0OOO0O0OO =='Relmax':#line:197
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=max (OOOOOO0O0O0OOOO00 )*1.0 /OO00O000OOOOOO00O .data ["rows_count"])#line:198
            if OOO0OO0O0OOO0O0OO =='Relmin':#line:199
                OOO00OOOOOO0O00OO =OOO00OOOOOO0O00OO and (OO00O000OOOOOO00O .quantifiers .get (OOO0OO0O0OOO0O0OO )<=min (OOOOOO0O0O0OOOO00 )*1.0 /OO00O000OOOOOO00O .data ["rows_count"])#line:200
        O0O0OOOO0O00O00O0 ={}#line:201
        if OOO00OOOOOO0O00OO ==True :#line:202
            OO00O000OOOOOO00O .stats ['total_valid']+=1 #line:204
            O0O0OOOO0O00O00O0 ["base"]=O0000O00OOO0O0OOO #line:205
            O0O0OOOO0O00O00O0 ["rel_base"]=O0000O00OOO0O0OOO *1.0 /OO00O000OOOOOO00O .data ["rows_count"]#line:206
            O0O0OOOO0O00O00O0 ["s_up"]=O000000O000000000 #line:207
            O0O0OOOO0O00O00O0 ["s_down"]=OO00O0O0OO000OO0O #line:208
            O0O0OOOO0O00O00O0 ["s_any_up"]=OO000OOO000O00OO0 #line:209
            O0O0OOOO0O00O00O0 ["s_any_down"]=O0000000O00OOO0O0 #line:210
            O0O0OOOO0O00O00O0 ["max"]=max (OOOOOO0O0O0OOOO00 )#line:211
            O0O0OOOO0O00O00O0 ["min"]=min (OOOOOO0O0O0OOOO00 )#line:212
            O0O0OOOO0O00O00O0 ["rel_max"]=max (OOOOOO0O0O0OOOO00 )*1.0 /OO00O000OOOOOO00O .data ["rows_count"]#line:213
            O0O0OOOO0O00O00O0 ["rel_min"]=min (OOOOOO0O0O0OOOO00 )*1.0 /OO00O000OOOOOO00O .data ["rows_count"]#line:214
            O0O0OOOO0O00O00O0 ["hist"]=OOOOOO0O0O0OOOO00 #line:215
        return OOO00OOOOOO0O00OO ,O0O0OOOO0O00O00O0 #line:217
    def _verify4ft (OO0OOO00O0OO000OO ,_O0O0O0OOO0O00OO0O ):#line:219
        O0O000O0OOOOO00O0 ={}#line:220
        for O0OO00OO0OO0OO0O0 in OO0OOO00O0OO000OO .task_actinfo ['cedents']:#line:221
            O0O000O0OOOOO00O0 [O0OO00OO0OO0OO0O0 ['cedent_type']]=O0OO00OO0OO0OO0O0 ['filter_value']#line:223
        O0OOO00OO0OO00O00 =bin (O0O000O0OOOOO00O0 ['ante']&O0O000O0OOOOO00O0 ['succ']&O0O000O0OOOOO00O0 ['cond']).count ("1")#line:225
        OOO00O0O00OOO00OO =None #line:226
        OOO00O0O00OOO00OO =0 #line:227
        if O0OOO00OO0OO00O00 >0 :#line:236
            OOO00O0O00OOO00OO =bin (O0O000O0OOOOO00O0 ['ante']&O0O000O0OOOOO00O0 ['succ']&O0O000O0OOOOO00O0 ['cond']).count ("1")*1.0 /bin (O0O000O0OOOOO00O0 ['ante']&O0O000O0OOOOO00O0 ['cond']).count ("1")#line:237
        OO00OOO0OO0O0OOOO =1 <<OO0OOO00O0OO000OO .data ["rows_count"]#line:239
        OO0000OO0000OO0OO =bin (O0O000O0OOOOO00O0 ['ante']&O0O000O0OOOOO00O0 ['succ']&O0O000O0OOOOO00O0 ['cond']).count ("1")#line:240
        OOO0O0O00O0OOO0O0 =bin (O0O000O0OOOOO00O0 ['ante']&~(OO00OOO0OO0O0OOOO |O0O000O0OOOOO00O0 ['succ'])&O0O000O0OOOOO00O0 ['cond']).count ("1")#line:241
        O0OO00OO0OO0OO0O0 =bin (~(OO00OOO0OO0O0OOOO |O0O000O0OOOOO00O0 ['ante'])&O0O000O0OOOOO00O0 ['succ']&O0O000O0OOOOO00O0 ['cond']).count ("1")#line:242
        OO0O0OO0O00000O0O =bin (~(OO00OOO0OO0O0OOOO |O0O000O0OOOOO00O0 ['ante'])&~(OO00OOO0OO0O0OOOO |O0O000O0OOOOO00O0 ['succ'])&O0O000O0OOOOO00O0 ['cond']).count ("1")#line:243
        OO0O0OO0OOO00OO0O =True #line:244
        for O0O0000OOOOOO00O0 in OO0OOO00O0OO000OO .quantifiers .keys ():#line:245
            if O0O0000OOOOOO00O0 =='Base':#line:246
                OO0O0OO0OOO00OO0O =OO0O0OO0OOO00OO0O and (OO0OOO00O0OO000OO .quantifiers .get (O0O0000OOOOOO00O0 )<=O0OOO00OO0OO00O00 )#line:247
            if O0O0000OOOOOO00O0 =='RelBase':#line:248
                OO0O0OO0OOO00OO0O =OO0O0OO0OOO00OO0O and (OO0OOO00O0OO000OO .quantifiers .get (O0O0000OOOOOO00O0 )<=O0OOO00OO0OO00O00 *1.0 /OO0OOO00O0OO000OO .data ["rows_count"])#line:249
            if O0O0000OOOOOO00O0 =='pim':#line:250
                OO0O0OO0OOO00OO0O =OO0O0OO0OOO00OO0O and (OO0OOO00O0OO000OO .quantifiers .get (O0O0000OOOOOO00O0 )<=OOO00O0O00OOO00OO )#line:251
        OO00OOOOO0OO00O00 ={}#line:252
        if OO0O0OO0OOO00OO0O ==True :#line:253
            OO0OOO00O0OO000OO .stats ['total_valid']+=1 #line:255
            OO00OOOOO0OO00O00 ["base"]=O0OOO00OO0OO00O00 #line:256
            OO00OOOOO0OO00O00 ["rel_base"]=O0OOO00OO0OO00O00 *1.0 /OO0OOO00O0OO000OO .data ["rows_count"]#line:257
            OO00OOOOO0OO00O00 ["pim"]=OOO00O0O00OOO00OO #line:258
            OO00OOOOO0OO00O00 ["fourfold"]=[OO0000OO0000OO0OO ,OOO0O0O00O0OOO0O0 ,O0OO00OO0OO0OO0O0 ,OO0O0OO0O00000O0O ]#line:259
        return OO0O0OO0OOO00OO0O ,OO00OOOOO0OO00O00 #line:261
    def _verifysd4ft (OOOO0O00O00OO0OO0 ,_OO0OO0O0O00OOO0OO ):#line:263
        O0O00OOO00O000O00 ={}#line:264
        for OO00O00O00000O00O in OOOO0O00O00OO0OO0 .task_actinfo ['cedents']:#line:265
            O0O00OOO00O000O00 [OO00O00O00000O00O ['cedent_type']]=OO00O00O00000O00O ['filter_value']#line:267
        OOOO0OOOOOO0OOOO0 =bin (O0O00OOO00O000O00 ['ante']&O0O00OOO00O000O00 ['succ']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['frst']).count ("1")#line:269
        O0OOO000O0O000000 =bin (O0O00OOO00O000O00 ['ante']&O0O00OOO00O000O00 ['succ']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['scnd']).count ("1")#line:270
        O0O00OO00O0OO00O0 =None #line:271
        OOOO00O00O0O0O00O =0 #line:272
        OO0OO0OOOO00OOOOO =0 #line:273
        if OOOO0OOOOOO0OOOO0 >0 :#line:282
            OOOO00O00O0O0O00O =bin (O0O00OOO00O000O00 ['ante']&O0O00OOO00O000O00 ['succ']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['frst']).count ("1")*1.0 /bin (O0O00OOO00O000O00 ['ante']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['frst']).count ("1")#line:283
        if O0OOO000O0O000000 >0 :#line:284
            OO0OO0OOOO00OOOOO =bin (O0O00OOO00O000O00 ['ante']&O0O00OOO00O000O00 ['succ']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['scnd']).count ("1")*1.0 /bin (O0O00OOO00O000O00 ['ante']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['scnd']).count ("1")#line:285
        OO000OO0O0OOOO000 =1 <<OOOO0O00O00OO0OO0 .data ["rows_count"]#line:287
        OOOOO0O0O0OOO0OOO =bin (O0O00OOO00O000O00 ['ante']&O0O00OOO00O000O00 ['succ']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['frst']).count ("1")#line:288
        OO00OO000OO000O00 =bin (O0O00OOO00O000O00 ['ante']&~(OO000OO0O0OOOO000 |O0O00OOO00O000O00 ['succ'])&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['frst']).count ("1")#line:289
        OO0O00O00OO0OO000 =bin (~(OO000OO0O0OOOO000 |O0O00OOO00O000O00 ['ante'])&O0O00OOO00O000O00 ['succ']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['frst']).count ("1")#line:290
        OO0O0OO0O0000O000 =bin (~(OO000OO0O0OOOO000 |O0O00OOO00O000O00 ['ante'])&~(OO000OO0O0OOOO000 |O0O00OOO00O000O00 ['succ'])&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['frst']).count ("1")#line:291
        O000OO00OO0O000O0 =bin (O0O00OOO00O000O00 ['ante']&O0O00OOO00O000O00 ['succ']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['scnd']).count ("1")#line:292
        O00OOO00O0O0O0O00 =bin (O0O00OOO00O000O00 ['ante']&~(OO000OO0O0OOOO000 |O0O00OOO00O000O00 ['succ'])&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['scnd']).count ("1")#line:293
        OO0OO0000O00OO0O0 =bin (~(OO000OO0O0OOOO000 |O0O00OOO00O000O00 ['ante'])&O0O00OOO00O000O00 ['succ']&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['scnd']).count ("1")#line:294
        OO000O0000OO00000 =bin (~(OO000OO0O0OOOO000 |O0O00OOO00O000O00 ['ante'])&~(OO000OO0O0OOOO000 |O0O00OOO00O000O00 ['succ'])&O0O00OOO00O000O00 ['cond']&O0O00OOO00O000O00 ['scnd']).count ("1")#line:295
        O00O00OO00OOO0O00 =True #line:296
        for O00OO0OOOOOOOOO0O in OOOO0O00O00OO0OO0 .quantifiers .keys ():#line:297
            if (O00OO0OOOOOOOOO0O =='FrstBase')|(O00OO0OOOOOOOOO0O =='Base1'):#line:298
                O00O00OO00OOO0O00 =O00O00OO00OOO0O00 and (OOOO0O00O00OO0OO0 .quantifiers .get (O00OO0OOOOOOOOO0O )<=OOOO0OOOOOO0OOOO0 )#line:299
            if (O00OO0OOOOOOOOO0O =='ScndBase')|(O00OO0OOOOOOOOO0O =='Base2'):#line:300
                O00O00OO00OOO0O00 =O00O00OO00OOO0O00 and (OOOO0O00O00OO0OO0 .quantifiers .get (O00OO0OOOOOOOOO0O )<=O0OOO000O0O000000 )#line:301
            if (O00OO0OOOOOOOOO0O =='FrstRelBase')|(O00OO0OOOOOOOOO0O =='RelBase1'):#line:302
                O00O00OO00OOO0O00 =O00O00OO00OOO0O00 and (OOOO0O00O00OO0OO0 .quantifiers .get (O00OO0OOOOOOOOO0O )<=OOOO0OOOOOO0OOOO0 *1.0 /OOOO0O00O00OO0OO0 .data ["rows_count"])#line:303
            if (O00OO0OOOOOOOOO0O =='ScndRelBase')|(O00OO0OOOOOOOOO0O =='RelBase2'):#line:304
                O00O00OO00OOO0O00 =O00O00OO00OOO0O00 and (OOOO0O00O00OO0OO0 .quantifiers .get (O00OO0OOOOOOOOO0O )<=O0OOO000O0O000000 *1.0 /OOOO0O00O00OO0OO0 .data ["rows_count"])#line:305
            if (O00OO0OOOOOOOOO0O =='Frstpim')|(O00OO0OOOOOOOOO0O =='pim1'):#line:306
                O00O00OO00OOO0O00 =O00O00OO00OOO0O00 and (OOOO0O00O00OO0OO0 .quantifiers .get (O00OO0OOOOOOOOO0O )<=OOOO00O00O0O0O00O )#line:307
            if (O00OO0OOOOOOOOO0O =='Scndpim')|(O00OO0OOOOOOOOO0O =='pim2'):#line:308
                O00O00OO00OOO0O00 =O00O00OO00OOO0O00 and (OOOO0O00O00OO0OO0 .quantifiers .get (O00OO0OOOOOOOOO0O )<=OO0OO0OOOO00OOOOO )#line:309
            if O00OO0OOOOOOOOO0O =='Deltapim':#line:310
                O00O00OO00OOO0O00 =O00O00OO00OOO0O00 and (OOOO0O00O00OO0OO0 .quantifiers .get (O00OO0OOOOOOOOO0O )<=OOOO00O00O0O0O00O -OO0OO0OOOO00OOOOO )#line:311
            if O00OO0OOOOOOOOO0O =='Ratiopim':#line:314
                if (OO0OO0OOOO00OOOOO >0 ):#line:315
                    O00O00OO00OOO0O00 =O00O00OO00OOO0O00 and (OOOO0O00O00OO0OO0 .quantifiers .get (O00OO0OOOOOOOOO0O )<=OOOO00O00O0O0O00O *1.0 /OO0OO0OOOO00OOOOO )#line:316
                else :#line:317
                    O00O00OO00OOO0O00 =False #line:318
        OO0OOOO0OO00OOOO0 ={}#line:319
        if O00O00OO00OOO0O00 ==True :#line:320
            OOOO0O00O00OO0OO0 .stats ['total_valid']+=1 #line:322
            OO0OOOO0OO00OOOO0 ["base1"]=OOOO0OOOOOO0OOOO0 #line:323
            OO0OOOO0OO00OOOO0 ["base2"]=O0OOO000O0O000000 #line:324
            OO0OOOO0OO00OOOO0 ["rel_base1"]=OOOO0OOOOOO0OOOO0 *1.0 /OOOO0O00O00OO0OO0 .rows_count #line:325
            OO0OOOO0OO00OOOO0 ["rel_base2"]=O0OOO000O0O000000 *1.0 /OOOO0O00O00OO0OO0 .rows_count #line:326
            OO0OOOO0OO00OOOO0 ["pim1"]=OOOO00O00O0O0O00O #line:327
            OO0OOOO0OO00OOOO0 ["pim2"]=OO0OO0OOOO00OOOOO #line:328
            OO0OOOO0OO00OOOO0 ["deltapim"]=OOOO00O00O0O0O00O -OO0OO0OOOO00OOOOO #line:329
            if (OO0OO0OOOO00OOOOO >0 ):#line:330
                OO0OOOO0OO00OOOO0 ["ratiopim"]=OOOO00O00O0O0O00O *1.0 /OO0OO0OOOO00OOOOO #line:331
            else :#line:332
                OO0OOOO0OO00OOOO0 ["ratiopim"]=None #line:333
            OO0OOOO0OO00OOOO0 ["fourfold1"]=[OOOOO0O0O0OOO0OOO ,OO00OO000OO000O00 ,OO0O00O00OO0OO000 ,OO0O0OO0O0000O000 ]#line:334
            OO0OOOO0OO00OOOO0 ["fourfold2"]=[O000OO00OO0O000O0 ,O00OOO00O0O0O0O00 ,OO0OO0000O00OO0O0 ,OO000O0000OO00000 ]#line:335
        return O00O00OO00OOO0O00 ,OO0OOOO0OO00OOOO0 #line:337
    def _verifynewact4ft (O0OO0000OO00O00O0 ,_O0OO0O0OO0OOOOO0O ):#line:339
        OOO0O0OO00OO0OOO0 ={}#line:340
        for O0OO0OOO0OO0OO0O0 in O0OO0000OO00O00O0 .task_actinfo ['cedents']:#line:341
            OOO0O0OO00OO0OOO0 [O0OO0OOO0OO0OO0O0 ['cedent_type']]=O0OO0OOO0OO0OO0O0 ['filter_value']#line:343
        O00OO00O000O0O00O =bin (OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['cond']).count ("1")#line:345
        O000O00OO000O0000 =bin (OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['cond']&OOO0O0OO00OO0OOO0 ['antv']&OOO0O0OO00OO0OOO0 ['sucv']).count ("1")#line:346
        O00OO0O000000O000 =None #line:347
        O00O00O00OOOO0OOO =0 #line:348
        O0OO0OOO000000OOO =0 #line:349
        if O00OO00O000O0O00O >0 :#line:358
            O00O00O00OOOO0OOO =bin (OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['cond']).count ("1")*1.0 /bin (OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['cond']).count ("1")#line:360
        if O000O00OO000O0000 >0 :#line:361
            O0OO0OOO000000OOO =bin (OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['cond']&OOO0O0OO00OO0OOO0 ['antv']&OOO0O0OO00OO0OOO0 ['sucv']).count ("1")*1.0 /bin (OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['cond']&OOO0O0OO00OO0OOO0 ['antv']).count ("1")#line:363
        O0O000O0OO0O0O000 =1 <<O0OO0000OO00O00O0 .rows_count #line:365
        OOO000OOO00O000OO =bin (OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['cond']).count ("1")#line:366
        OOOOO000O00OOOO0O =bin (OOO0O0OO00OO0OOO0 ['ante']&~(O0O000O0OO0O0O000 |OOO0O0OO00OO0OOO0 ['succ'])&OOO0O0OO00OO0OOO0 ['cond']).count ("1")#line:367
        O00O0000OO0OOOOO0 =bin (~(O0O000O0OO0O0O000 |OOO0O0OO00OO0OOO0 ['ante'])&OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['cond']).count ("1")#line:368
        OO000000OO0O0O0OO =bin (~(O0O000O0OO0O0O000 |OOO0O0OO00OO0OOO0 ['ante'])&~(O0O000O0OO0O0O000 |OOO0O0OO00OO0OOO0 ['succ'])&OOO0O0OO00OO0OOO0 ['cond']).count ("1")#line:369
        OO0O0OO0O0O0O0OOO =bin (OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['cond']&OOO0O0OO00OO0OOO0 ['antv']&OOO0O0OO00OO0OOO0 ['sucv']).count ("1")#line:370
        OO0000OO0OO00O00O =bin (OOO0O0OO00OO0OOO0 ['ante']&~(O0O000O0OO0O0O000 |(OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['sucv']))&OOO0O0OO00OO0OOO0 ['cond']).count ("1")#line:371
        OOO00O00O0OO00OOO =bin (~(O0O000O0OO0O0O000 |(OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['antv']))&OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['cond']&OOO0O0OO00OO0OOO0 ['sucv']).count ("1")#line:372
        O0OOO0OO00O0OO0OO =bin (~(O0O000O0OO0O0O000 |(OOO0O0OO00OO0OOO0 ['ante']&OOO0O0OO00OO0OOO0 ['antv']))&~(O0O000O0OO0O0O000 |(OOO0O0OO00OO0OOO0 ['succ']&OOO0O0OO00OO0OOO0 ['sucv']))&OOO0O0OO00OO0OOO0 ['cond']).count ("1")#line:373
        O00OOO00OO0O000O0 =True #line:374
        for O000OO0OO0O0O00O0 in O0OO0000OO00O00O0 .quantifiers .keys ():#line:375
            if (O000OO0OO0O0O00O0 =='PreBase')|(O000OO0OO0O0O00O0 =='Base1'):#line:376
                O00OOO00OO0O000O0 =O00OOO00OO0O000O0 and (O0OO0000OO00O00O0 .quantifiers .get (O000OO0OO0O0O00O0 )<=O00OO00O000O0O00O )#line:377
            if (O000OO0OO0O0O00O0 =='PostBase')|(O000OO0OO0O0O00O0 =='Base2'):#line:378
                O00OOO00OO0O000O0 =O00OOO00OO0O000O0 and (O0OO0000OO00O00O0 .quantifiers .get (O000OO0OO0O0O00O0 )<=O000O00OO000O0000 )#line:379
            if (O000OO0OO0O0O00O0 =='PreRelBase')|(O000OO0OO0O0O00O0 =='RelBase1'):#line:380
                O00OOO00OO0O000O0 =O00OOO00OO0O000O0 and (O0OO0000OO00O00O0 .quantifiers .get (O000OO0OO0O0O00O0 )<=O00OO00O000O0O00O *1.0 /O0OO0000OO00O00O0 .data ["rows_count"])#line:381
            if (O000OO0OO0O0O00O0 =='PostRelBase')|(O000OO0OO0O0O00O0 =='RelBase2'):#line:382
                O00OOO00OO0O000O0 =O00OOO00OO0O000O0 and (O0OO0000OO00O00O0 .quantifiers .get (O000OO0OO0O0O00O0 )<=O000O00OO000O0000 *1.0 /O0OO0000OO00O00O0 .data ["rows_count"])#line:383
            if (O000OO0OO0O0O00O0 =='Prepim')|(O000OO0OO0O0O00O0 =='pim1'):#line:384
                O00OOO00OO0O000O0 =O00OOO00OO0O000O0 and (O0OO0000OO00O00O0 .quantifiers .get (O000OO0OO0O0O00O0 )<=O00O00O00OOOO0OOO )#line:385
            if (O000OO0OO0O0O00O0 =='Postpim')|(O000OO0OO0O0O00O0 =='pim2'):#line:386
                O00OOO00OO0O000O0 =O00OOO00OO0O000O0 and (O0OO0000OO00O00O0 .quantifiers .get (O000OO0OO0O0O00O0 )<=O0OO0OOO000000OOO )#line:387
            if O000OO0OO0O0O00O0 =='Deltapim':#line:388
                O00OOO00OO0O000O0 =O00OOO00OO0O000O0 and (O0OO0000OO00O00O0 .quantifiers .get (O000OO0OO0O0O00O0 )<=O00O00O00OOOO0OOO -O0OO0OOO000000OOO )#line:389
            if O000OO0OO0O0O00O0 =='Ratiopim':#line:392
                if (O0OO0OOO000000OOO >0 ):#line:393
                    O00OOO00OO0O000O0 =O00OOO00OO0O000O0 and (O0OO0000OO00O00O0 .quantifiers .get (O000OO0OO0O0O00O0 )<=O00O00O00OOOO0OOO *1.0 /O0OO0OOO000000OOO )#line:394
                else :#line:395
                    O00OOO00OO0O000O0 =False #line:396
        OOOOOOO0OOO00O0OO ={}#line:397
        if O00OOO00OO0O000O0 ==True :#line:398
            O0OO0000OO00O00O0 .stats ['total_valid']+=1 #line:400
            OOOOOOO0OOO00O0OO ["base1"]=O00OO00O000O0O00O #line:401
            OOOOOOO0OOO00O0OO ["base2"]=O000O00OO000O0000 #line:402
            OOOOOOO0OOO00O0OO ["rel_base1"]=O00OO00O000O0O00O *1.0 /O0OO0000OO00O00O0 .data ["rows_count"]#line:403
            OOOOOOO0OOO00O0OO ["rel_base2"]=O000O00OO000O0000 *1.0 /O0OO0000OO00O00O0 .data ["rows_count"]#line:404
            OOOOOOO0OOO00O0OO ["pim1"]=O00O00O00OOOO0OOO #line:405
            OOOOOOO0OOO00O0OO ["pim2"]=O0OO0OOO000000OOO #line:406
            OOOOOOO0OOO00O0OO ["deltapim"]=O00O00O00OOOO0OOO -O0OO0OOO000000OOO #line:407
            if (O0OO0OOO000000OOO >0 ):#line:408
                OOOOOOO0OOO00O0OO ["ratiopim"]=O00O00O00OOOO0OOO *1.0 /O0OO0OOO000000OOO #line:409
            else :#line:410
                OOOOOOO0OOO00O0OO ["ratiopim"]=None #line:411
            OOOOOOO0OOO00O0OO ["fourfoldpre"]=[OOO000OOO00O000OO ,OOOOO000O00OOOO0O ,O00O0000OO0OOOOO0 ,OO000000OO0O0O0OO ]#line:412
            OOOOOOO0OOO00O0OO ["fourfoldpost"]=[OO0O0OO0O0O0O0OOO ,OO0000OO0OO00O00O ,OOO00O00O0OO00OOO ,O0OOO0OO00O0OO0OO ]#line:413
        return O00OOO00OO0O000O0 ,OOOOOOO0OOO00O0OO #line:415
    def _verifyact4ft (O0OOO0OO000000000 ,_OO0OO0O000OOO00OO ):#line:417
        OO00OO0O0000O0O00 ={}#line:418
        for O000OOOOOOOO00O0O in O0OOO0OO000000000 .task_actinfo ['cedents']:#line:419
            OO00OO0O0000O0O00 [O000OOOOOOOO00O0O ['cedent_type']]=O000OOOOOOOO00O0O ['filter_value']#line:421
        O0O0OOO00OOOO0O00 =bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['antv-']&OO00OO0O0000O0O00 ['sucv-']).count ("1")#line:423
        O0OOOOO0OO00O0O00 =bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['antv+']&OO00OO0O0000O0O00 ['sucv+']).count ("1")#line:424
        O00OOOO0OOO000OO0 =None #line:425
        O0O00O0OOOOO000O0 =0 #line:426
        O000OOO00O0O0OOO0 =0 #line:427
        if O0O0OOO00OOOO0O00 >0 :#line:436
            O0O00O0OOOOO000O0 =bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['antv-']&OO00OO0O0000O0O00 ['sucv-']).count ("1")*1.0 /bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['antv-']).count ("1")#line:438
        if O0OOOOO0OO00O0O00 >0 :#line:439
            O000OOO00O0O0OOO0 =bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['antv+']&OO00OO0O0000O0O00 ['sucv+']).count ("1")*1.0 /bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['antv+']).count ("1")#line:441
        OOO0O00O000OOO0O0 =1 <<O0OOO0OO000000000 .data ["rows_count"]#line:443
        O000OOOOOOO00OOO0 =bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['antv-']&OO00OO0O0000O0O00 ['sucv-']).count ("1")#line:444
        O00O000OO0O0O0O00 =bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['antv-']&~(OOO0O00O000OOO0O0 |(OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['sucv-']))&OO00OO0O0000O0O00 ['cond']).count ("1")#line:445
        O0OO00OOOOOO0O00O =bin (~(OOO0O00O000OOO0O0 |(OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['antv-']))&OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['sucv-']).count ("1")#line:446
        OOO0O0O0O00O000OO =bin (~(OOO0O00O000OOO0O0 |(OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['antv-']))&~(OOO0O00O000OOO0O0 |(OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['sucv-']))&OO00OO0O0000O0O00 ['cond']).count ("1")#line:447
        OO0OOOO0OO00OO0OO =bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['antv+']&OO00OO0O0000O0O00 ['sucv+']).count ("1")#line:448
        O00O0000O0O0OO00O =bin (OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['antv+']&~(OOO0O00O000OOO0O0 |(OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['sucv+']))&OO00OO0O0000O0O00 ['cond']).count ("1")#line:449
        OOOOO000000OO0O00 =bin (~(OOO0O00O000OOO0O0 |(OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['antv+']))&OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['cond']&OO00OO0O0000O0O00 ['sucv+']).count ("1")#line:450
        O00OO00OOO000OOOO =bin (~(OOO0O00O000OOO0O0 |(OO00OO0O0000O0O00 ['ante']&OO00OO0O0000O0O00 ['antv+']))&~(OOO0O00O000OOO0O0 |(OO00OO0O0000O0O00 ['succ']&OO00OO0O0000O0O00 ['sucv+']))&OO00OO0O0000O0O00 ['cond']).count ("1")#line:451
        O0O0OO0000OO00O0O =True #line:452
        for O0O000000000000OO in O0OOO0OO000000000 .quantifiers .keys ():#line:453
            if (O0O000000000000OO =='PreBase')|(O0O000000000000OO =='Base1'):#line:454
                O0O0OO0000OO00O0O =O0O0OO0000OO00O0O and (O0OOO0OO000000000 .quantifiers .get (O0O000000000000OO )<=O0O0OOO00OOOO0O00 )#line:455
            if (O0O000000000000OO =='PostBase')|(O0O000000000000OO =='Base2'):#line:456
                O0O0OO0000OO00O0O =O0O0OO0000OO00O0O and (O0OOO0OO000000000 .quantifiers .get (O0O000000000000OO )<=O0OOOOO0OO00O0O00 )#line:457
            if (O0O000000000000OO =='PreRelBase')|(O0O000000000000OO =='RelBase1'):#line:458
                O0O0OO0000OO00O0O =O0O0OO0000OO00O0O and (O0OOO0OO000000000 .quantifiers .get (O0O000000000000OO )<=O0O0OOO00OOOO0O00 *1.0 /O0OOO0OO000000000 .data ["rows_count"])#line:459
            if (O0O000000000000OO =='PostRelBase')|(O0O000000000000OO =='RelBase2'):#line:460
                O0O0OO0000OO00O0O =O0O0OO0000OO00O0O and (O0OOO0OO000000000 .quantifiers .get (O0O000000000000OO )<=O0OOOOO0OO00O0O00 *1.0 /O0OOO0OO000000000 .data ["rows_count"])#line:461
            if (O0O000000000000OO =='Prepim')|(O0O000000000000OO =='pim1'):#line:462
                O0O0OO0000OO00O0O =O0O0OO0000OO00O0O and (O0OOO0OO000000000 .quantifiers .get (O0O000000000000OO )<=O0O00O0OOOOO000O0 )#line:463
            if (O0O000000000000OO =='Postpim')|(O0O000000000000OO =='pim2'):#line:464
                O0O0OO0000OO00O0O =O0O0OO0000OO00O0O and (O0OOO0OO000000000 .quantifiers .get (O0O000000000000OO )<=O000OOO00O0O0OOO0 )#line:465
            if O0O000000000000OO =='Deltapim':#line:466
                O0O0OO0000OO00O0O =O0O0OO0000OO00O0O and (O0OOO0OO000000000 .quantifiers .get (O0O000000000000OO )<=O0O00O0OOOOO000O0 -O000OOO00O0O0OOO0 )#line:467
            if O0O000000000000OO =='Ratiopim':#line:470
                if (O0O00O0OOOOO000O0 >0 ):#line:471
                    O0O0OO0000OO00O0O =O0O0OO0000OO00O0O and (O0OOO0OO000000000 .quantifiers .get (O0O000000000000OO )<=O000OOO00O0O0OOO0 *1.0 /O0O00O0OOOOO000O0 )#line:472
                else :#line:473
                    O0O0OO0000OO00O0O =False #line:474
        OOOO0O00OOOOO0O00 ={}#line:475
        if O0O0OO0000OO00O0O ==True :#line:476
            O0OOO0OO000000000 .stats ['total_valid']+=1 #line:478
            OOOO0O00OOOOO0O00 ["base1"]=O0O0OOO00OOOO0O00 #line:479
            OOOO0O00OOOOO0O00 ["base2"]=O0OOOOO0OO00O0O00 #line:480
            OOOO0O00OOOOO0O00 ["rel_base1"]=O0O0OOO00OOOO0O00 *1.0 /O0OOO0OO000000000 .data ["rows_count"]#line:481
            OOOO0O00OOOOO0O00 ["rel_base2"]=O0OOOOO0OO00O0O00 *1.0 /O0OOO0OO000000000 .data ["rows_count"]#line:482
            OOOO0O00OOOOO0O00 ["pim1"]=O0O00O0OOOOO000O0 #line:483
            OOOO0O00OOOOO0O00 ["pim2"]=O000OOO00O0O0OOO0 #line:484
            OOOO0O00OOOOO0O00 ["deltapim"]=O0O00O0OOOOO000O0 -O000OOO00O0O0OOO0 #line:485
            if (O0O00O0OOOOO000O0 >0 ):#line:486
                OOOO0O00OOOOO0O00 ["ratiopim"]=O000OOO00O0O0OOO0 *1.0 /O0O00O0OOOOO000O0 #line:487
            else :#line:488
                OOOO0O00OOOOO0O00 ["ratiopim"]=None #line:489
            OOOO0O00OOOOO0O00 ["fourfoldpre"]=[O000OOOOOOO00OOO0 ,O00O000OO0O0O0O00 ,O0OO00OOOOOO0O00O ,OOO0O0O0O00O000OO ]#line:490
            OOOO0O00OOOOO0O00 ["fourfoldpost"]=[OO0OOOO0OO00OO0OO ,O00O0000O0O0OO00O ,OOOOO000000OO0O00 ,O00OO00OOO000OOOO ]#line:491
        return O0O0OO0000OO00O0O ,OOOO0O00OOOOO0O00 #line:493
    def _print (O0000OO0O0O00OO00 ,OOOOOOOO0OO0O00OO ,_OO0OOO000O00OO000 ,_OOOO0O00OO000OO0O ):#line:495
        if (len (_OO0OOO000O00OO000 ))!=len (_OOOO0O00OO000OO0O ):#line:496
            print ("DIFF IN LEN for following cedent : "+str (len (_OO0OOO000O00OO000 ))+" vs "+str (len (_OOOO0O00OO000OO0O )))#line:497
            print ("trace cedent : "+str (_OO0OOO000O00OO000 )+", traces "+str (_OOOO0O00OO000OO0O ))#line:498
        OO00O0O0OO0O00O0O =''#line:499
        for O0OO0OO0OO00OO000 in range (len (_OO0OOO000O00OO000 )):#line:500
            OO0O0OO000000OO00 =O0000OO0O0O00OO00 .data ["varname"].index (OOOOOOOO0OO0O00OO ['defi'].get ('attributes')[_OO0OOO000O00OO000 [O0OO0OO0OO00OO000 ]].get ('name'))#line:501
            OO00O0O0OO0O00O0O =OO00O0O0OO0O00O0O +O0000OO0O0O00OO00 .data ["varname"][OO0O0OO000000OO00 ]+'('#line:503
            for O00OOOO0OO0O000OO in _OOOO0O00OO000OO0O [O0OO0OO0OO00OO000 ]:#line:504
                OO00O0O0OO0O00O0O =OO00O0O0OO0O00O0O +O0000OO0O0O00OO00 .data ["catnames"][OO0O0OO000000OO00 ][O00OOOO0OO0O000OO ]+" "#line:505
            OO00O0O0OO0O00O0O =OO00O0O0OO0O00O0O +')'#line:506
            if O0OO0OO0OO00OO000 +1 <len (_OO0OOO000O00OO000 ):#line:507
                OO00O0O0OO0O00O0O =OO00O0O0OO0O00O0O +' & '#line:508
        return OO00O0O0OO0O00O0O #line:512
    def _print_hypo (O0OO0O0000O0OOOO0 ,OOOO0O00OO0OOOOO0 ):#line:514
        print ('Hypothesis info : '+str (OOOO0O00OO0OOOOO0 ['params']))#line:515
        for OO00O0OO0OO0O000O in O0OO0O0000O0OOOO0 .task_actinfo ['cedents']:#line:516
            print (OO00O0OO0OO0O000O ['cedent_type']+' = '+OO00O0OO0OO0O000O ['generated_string'])#line:517
    def _genvar (OOO000OOO0OO0OO00 ,OO000O0OOOOOOOOO0 ,OOOO00000O0000O00 ,_OO000O0O000000O0O ,_OO00O00OOOOOOOOO0 ,_OOOO0000O0OOOOO0O ,_OOOOO00O0O00OOOOO ,_O0000O00O0OOOOO00 ):#line:519
        for OO000O0O0O0OO000O in range (OOOO00000O0000O00 ['num_cedent']):#line:520
            if len (_OO000O0O000000O0O )==0 or OO000O0O0O0OO000O >_OO000O0O000000O0O [-1 ]:#line:521
                _OO000O0O000000O0O .append (OO000O0O0O0OO000O )#line:522
                O0000O000OO00OO00 =OOO000OOO0OO0OO00 .data ["varname"].index (OOOO00000O0000O00 ['defi'].get ('attributes')[OO000O0O0O0OO000O ].get ('name'))#line:523
                _O00O00O0000O00OOO =OOOO00000O0000O00 ['defi'].get ('attributes')[OO000O0O0O0OO000O ].get ('minlen')#line:524
                _OOO0OO0OOO0O00OOO =OOOO00000O0000O00 ['defi'].get ('attributes')[OO000O0O0O0OO000O ].get ('maxlen')#line:525
                _OO0O0OO00OOO00OOO =OOOO00000O0000O00 ['defi'].get ('attributes')[OO000O0O0O0OO000O ].get ('type')#line:526
                OO00OOO00OO0O0O0O =len (OOO000OOO0OO0OO00 .data ["dm"][O0000O000OO00OO00 ])#line:527
                _OOOO0OOO0OOO00OOO =[]#line:528
                _OO00O00OOOOOOOOO0 .append (_OOOO0OOO0OOO00OOO )#line:529
                _O0000OOO0O00O0OOO =int (0 )#line:530
                OOO000OOO0OO0OO00 ._gencomb (OO000O0OOOOOOOOO0 ,OOOO00000O0000O00 ,_OO000O0O000000O0O ,_OO00O00OOOOOOOOO0 ,_OOOO0OOO0OOO00OOO ,_OOOO0000O0OOOOO0O ,_O0000OOO0O00O0OOO ,OO00OOO00OO0O0O0O ,_OO0O0OO00OOO00OOO ,_OOOOO00O0O00OOOOO ,_O0000O00O0OOOOO00 ,_O00O00O0000O00OOO ,_OOO0OO0OOO0O00OOO )#line:531
                _OO00O00OOOOOOOOO0 .pop ()#line:532
                _OO000O0O000000O0O .pop ()#line:533
    def _gencomb (O0OO0O0OOOO0O00OO ,OOOO0O00O0OO0O0OO ,O0OOOOOOOOOO000OO ,_OOOOO0OO0OO0O0000 ,_OO0OOOO0O0OOOO0OO ,_OO0O00O0O000000O0 ,_OO0000O00OO00000O ,_OO0O00O0O0O0O0000 ,OO00O0O00OOO000OO ,_O000O00OO00OOO00O ,_O0OOOO0O00O0OO0O0 ,_OO00000O0O0OO0O0O ,_OOO0OO0OOO00O0OOO ,_O00OOO0000O000000 ):#line:535
        _O00OOOOOOOOOOOOOO =[]#line:536
        if _O000O00OO00OOO00O =="subset":#line:537
            if len (_OO0O00O0O000000O0 )==0 :#line:538
                _O00OOOOOOOOOOOOOO =range (OO00O0O00OOO000OO )#line:539
            else :#line:540
                _O00OOOOOOOOOOOOOO =range (_OO0O00O0O000000O0 [-1 ]+1 ,OO00O0O00OOO000OO )#line:541
        elif _O000O00OO00OOO00O =="seq":#line:542
            if len (_OO0O00O0O000000O0 )==0 :#line:543
                _O00OOOOOOOOOOOOOO =range (OO00O0O00OOO000OO -_OOO0OO0OOO00O0OOO +1 )#line:544
            else :#line:545
                if _OO0O00O0O000000O0 [-1 ]+1 ==OO00O0O00OOO000OO :#line:546
                    return #line:547
                O000000O0O000O0OO =_OO0O00O0O000000O0 [-1 ]+1 #line:548
                _O00OOOOOOOOOOOOOO .append (O000000O0O000O0OO )#line:549
        elif _O000O00OO00OOO00O =="lcut":#line:550
            if len (_OO0O00O0O000000O0 )==0 :#line:551
                O000000O0O000O0OO =0 ;#line:552
            else :#line:553
                if _OO0O00O0O000000O0 [-1 ]+1 ==OO00O0O00OOO000OO :#line:554
                    return #line:555
                O000000O0O000O0OO =_OO0O00O0O000000O0 [-1 ]+1 #line:556
            _O00OOOOOOOOOOOOOO .append (O000000O0O000O0OO )#line:557
        elif _O000O00OO00OOO00O =="rcut":#line:558
            if len (_OO0O00O0O000000O0 )==0 :#line:559
                O000000O0O000O0OO =OO00O0O00OOO000OO -1 ;#line:560
            else :#line:561
                if _OO0O00O0O000000O0 [-1 ]==0 :#line:562
                    return #line:563
                O000000O0O000O0OO =_OO0O00O0O000000O0 [-1 ]-1 #line:564
            _O00OOOOOOOOOOOOOO .append (O000000O0O000O0OO )#line:566
        else :#line:567
            print ("Attribute type "+_O000O00OO00OOO00O +" not supported.")#line:568
            return #line:569
        for OOO0O00OO00OO0O00 in _O00OOOOOOOOOOOOOO :#line:572
                _OO0O00O0O000000O0 .append (OOO0O00OO00OO0O00 )#line:574
                _OO0OOOO0O0OOOO0OO .pop ()#line:575
                _OO0OOOO0O0OOOO0OO .append (_OO0O00O0O000000O0 )#line:576
                _OOO0000O0O0O0O000 =_OO0O00O0O0O0O0000 |O0OO0O0OOOO0O00OO .data ["dm"][O0OO0O0OOOO0O00OO .data ["varname"].index (O0OOOOOOOOOO000OO ['defi'].get ('attributes')[_OOOOO0OO0OO0O0000 [-1 ]].get ('name'))][OOO0O00OO00OO0O00 ]#line:580
                _O0O00000000O0OOO0 =1 #line:582
                if (len (_OOOOO0OO0OO0O0000 )<_O0OOOO0O00O0OO0O0 ):#line:583
                    _O0O00000000O0OOO0 =0 #line:584
                if (len (_OO0OOOO0O0OOOO0OO [-1 ])>=_OOO0OO0OOO00O0OOO ):#line:585
                    _OOOOO0O0O00000O0O =0 #line:586
                    if O0OOOOOOOOOO000OO ['defi'].get ('type')=='con':#line:587
                        _OOOOO0O0O00000O0O =_OO0000O00OO00000O &_OOO0000O0O0O0O000 #line:588
                    else :#line:589
                        _OOOOO0O0O00000O0O =_OO0000O00OO00000O |_OOO0000O0O0O0O000 #line:590
                    if _O0O00000000O0OOO0 ==1 :#line:591
                        O0OOOOOOOOOO000OO ['trace_cedent']=_OOOOO0OO0OO0O0000 #line:592
                        O0OOOOOOOOOO000OO ['traces']=_OO0OOOO0O0OOOO0OO #line:593
                        O0OOOOOOOOOO000OO ['generated_string']=O0OO0O0OOOO0O00OO ._print (O0OOOOOOOOOO000OO ,_OOOOO0OO0OO0O0000 ,_OO0OOOO0O0OOOO0OO )#line:594
                        O0OOOOOOOOOO000OO ['filter_value']=_OOOOO0O0O00000O0O #line:595
                        OOOO0O00O0OO0O0OO ['cedents'].append (O0OOOOOOOOOO000OO )#line:596
                        if len (OOOO0O00O0OO0O0OO ['cedents_to_do'])==len (OOOO0O00O0OO0O0OO ['cedents']):#line:597
                            if O0OO0O0OOOO0O00OO .proc =='CFMiner':#line:598
                                O0OOO00O00OO0O00O ,O0OOO0OO00OOO0O0O =O0OO0O0OOOO0O00OO ._verifyCF (_OOOOO0O0O00000O0O )#line:599
                            elif O0OO0O0OOOO0O00OO .proc =='4ftMiner':#line:600
                                O0OOO00O00OO0O00O ,O0OOO0OO00OOO0O0O =O0OO0O0OOOO0O00OO ._verify4ft (_OOO0000O0O0O0O000 )#line:601
                            elif O0OO0O0OOOO0O00OO .proc =='SD4ftMiner':#line:602
                                O0OOO00O00OO0O00O ,O0OOO0OO00OOO0O0O =O0OO0O0OOOO0O00OO ._verifysd4ft (_OOO0000O0O0O0O000 )#line:603
                            elif O0OO0O0OOOO0O00OO .proc =='NewAct4ftMiner':#line:604
                                O0OOO00O00OO0O00O ,O0OOO0OO00OOO0O0O =O0OO0O0OOOO0O00OO ._verifynewact4ft (_OOO0000O0O0O0O000 )#line:605
                            elif O0OO0O0OOOO0O00OO .proc =='Act4ftMiner':#line:606
                                O0OOO00O00OO0O00O ,O0OOO0OO00OOO0O0O =O0OO0O0OOOO0O00OO ._verifyact4ft (_OOO0000O0O0O0O000 )#line:607
                            else :#line:608
                                print ("Unsupported procedure : "+O0OO0O0OOOO0O00OO .proc )#line:609
                                exit (0 )#line:610
                            if O0OOO00O00OO0O00O ==True :#line:611
                                OOOOOOOO00O0OO000 ={}#line:612
                                OOOOOOOO00O0OO000 ["hypo_id"]=O0OO0O0OOOO0O00OO .stats ['total_valid']#line:613
                                OOOOOOOO00O0OO000 ["cedents"]={}#line:614
                                for O000O0OO00O000000 in OOOO0O00O0OO0O0OO ['cedents']:#line:615
                                    OOOOOOOO00O0OO000 ['cedents'][O000O0OO00O000000 ['cedent_type']]=O000O0OO00O000000 ['generated_string']#line:616
                                OOOOOOOO00O0OO000 ["params"]=O0OOO0OO00OOO0O0O #line:618
                                OOOOOOOO00O0OO000 ["trace_cedent"]=_OOOOO0OO0OO0O0000 #line:619
                                O0OO0O0OOOO0O00OO ._print_hypo (OOOOOOOO00O0OO000 )#line:620
                                OOOOOOOO00O0OO000 ["traces"]=_OO0OOOO0O0OOOO0OO #line:623
                                O0OO0O0OOOO0O00OO .hypolist .append (OOOOOOOO00O0OO000 )#line:624
                        else :#line:625
                            O0OO0O0OOOO0O00OO ._start_cedent (OOOO0O00O0OO0O0OO )#line:626
                        OOOO0O00O0OO0O0OO ['cedents'].pop ()#line:627
                    if (len (_OOOOO0OO0OO0O0000 )<_OO00000O0O0OO0O0O ):#line:628
                        O0OO0O0OOOO0O00OO ._genvar (OOOO0O00O0OO0O0OO ,O0OOOOOOOOOO000OO ,_OOOOO0OO0OO0O0000 ,_OO0OOOO0O0OOOO0OO ,_OOOOO0O0O00000O0O ,_O0OOOO0O00O0OO0O0 ,_OO00000O0O0OO0O0O )#line:629
                O0OO0O0OOOO0O00OO .stats ['total_cnt']+=1 #line:630
                if len (_OO0O00O0O000000O0 )<_O00OOO0000O000000 :#line:631
                    O0OO0O0OOOO0O00OO ._gencomb (OOOO0O00O0OO0O0OO ,O0OOOOOOOOOO000OO ,_OOOOO0OO0OO0O0000 ,_OO0OOOO0O0OOOO0OO ,_OO0O00O0O000000O0 ,_OO0000O00OO00000O ,_OOO0000O0O0O0O000 ,OO00O0O00OOO000OO ,_O000O00OO00OOO00O ,_O0OOOO0O00O0OO0O0 ,_OO00000O0O0OO0O0O ,_OOO0OO0OOO00O0OOO ,_O00OOO0000O000000 )#line:632
                _OO0O00O0O000000O0 .pop ()#line:633
    def _start_cedent (O000O0O0OO00O0OOO ,OOOO0O000OOOO00O0 ):#line:635
        if len (OOOO0O000OOOO00O0 ['cedents_to_do'])>len (OOOO0O000OOOO00O0 ['cedents']):#line:636
            _O00OO00O0O0O0O00O =[]#line:637
            _OO00000O0OOO0O0OO =[]#line:638
            O000O00OO0O0OO0O0 ={}#line:639
            O000O00OO0O0OO0O0 ['cedent_type']=OOOO0O000OOOO00O0 ['cedents_to_do'][len (OOOO0O000OOOO00O0 ['cedents'])]#line:640
            O0O00O00O0OOO000O =O000O00OO0O0OO0O0 ['cedent_type']#line:641
            if ((O0O00O00O0OOO000O [-1 ]=='-')|(O0O00O00O0OOO000O [-1 ]=='+')):#line:642
                O0O00O00O0OOO000O =O0O00O00O0OOO000O [:-1 ]#line:643
            O000O00OO0O0OO0O0 ['defi']=O000O0O0OO00O0OOO .kwargs .get (O0O00O00O0OOO000O )#line:645
            if (O000O00OO0O0OO0O0 ['defi']==None ):#line:646
                print ("Error getting cedent ",O000O00OO0O0OO0O0 ['cedent_type'])#line:647
            _O0000O0000O0OO00O =int (0 )#line:648
            O000O00OO0O0OO0O0 ['num_cedent']=len (O000O00OO0O0OO0O0 ['defi'].get ('attributes'))#line:653
            if (O000O00OO0O0OO0O0 ['defi'].get ('type')=='con'):#line:654
                _O0000O0000O0OO00O =(1 <<O000O0O0OO00O0OOO .data ["rows_count"])-1 #line:655
            O000O0O0OO00O0OOO ._genvar (OOOO0O000OOOO00O0 ,O000O00OO0O0OO0O0 ,_O00OO00O0O0O0O00O ,_OO00000O0OOO0O0OO ,_O0000O0000O0OO00O ,O000O00OO0O0OO0O0 ['defi'].get ('minlen'),O000O00OO0O0OO0O0 ['defi'].get ('maxlen'))#line:656
    def _calc_all (O000O0OO00O0O000O ,**OO0O0O0O00OO00OO0 ):#line:659
        O000O0OO00O0O000O ._prep_data (O000O0OO00O0O000O .kwargs .get ("df"))#line:660
        O000O0OO00O0O000O ._calculate (**OO0O0O0O00OO00OO0 )#line:661
    def _calculate (OOOOOOO0OO00O0OO0 ,**O00O0O000O0OO0O00 ):#line:663
        if OOOOOOO0OO00O0OO0 .data ["data_prepared"]==0 :#line:664
            print ("Error: data not prepared")#line:665
            return #line:666
        OOOOOOO0OO00O0OO0 .kwargs =O00O0O000O0OO0O00 #line:667
        OOOOOOO0OO00O0OO0 .proc =O00O0O000O0OO0O00 .get ('proc')#line:668
        OOOOOOO0OO00O0OO0 .quantifiers =O00O0O000O0OO0O00 .get ('quantifiers')#line:669
        OOOOOOO0OO00O0OO0 ._init_task ()#line:671
        OOOOOOO0OO00O0OO0 .stats ['start_proc_time']=time .time ()#line:672
        OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do']=[]#line:673
        OOOOOOO0OO00O0OO0 .task_actinfo ['cedents']=[]#line:674
        if O00O0O000O0OO0O00 .get ("proc")=='CFMiner':#line:676
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do']=['cond']#line:677
        elif O00O0O000O0OO0O00 .get ("proc")=='4ftMiner':#line:678
            _OO0O0OO0000O0OOOO =O00O0O000O0OO0O00 .get ("cond")#line:679
            if _OO0O0OO0000O0OOOO !=None :#line:680
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:681
            else :#line:682
                O00O0O000O0OO000O =OOOOOOO0OO00O0OO0 .cedent #line:683
                O00O0O000O0OO000O ['cedent_type']='cond'#line:684
                O00O0O000O0OO000O ['filter_value']=(1 <<OOOOOOO0OO00O0OO0 .data ["rows_count"])-1 #line:685
                O00O0O000O0OO000O ['generated_string']='---'#line:686
                print (O00O0O000O0OO000O ['filter_value'])#line:687
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:688
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents'].append (O00O0O000O0OO000O )#line:689
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:693
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:694
        elif O00O0O000O0OO0O00 .get ("proc")=='NewAct4ftMiner':#line:695
            _OO0O0OO0000O0OOOO =O00O0O000O0OO0O00 .get ("cond")#line:698
            if _OO0O0OO0000O0OOOO !=None :#line:699
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:700
            else :#line:701
                O00O0O000O0OO000O =OOOOOOO0OO00O0OO0 .cedent #line:702
                O00O0O000O0OO000O ['cedent_type']='cond'#line:703
                O00O0O000O0OO000O ['filter_value']=(1 <<OOOOOOO0OO00O0OO0 .data ["rows_count"])-1 #line:704
                O00O0O000O0OO000O ['generated_string']='---'#line:705
                print (O00O0O000O0OO000O ['filter_value'])#line:706
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:707
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents'].append (O00O0O000O0OO000O )#line:708
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('antv')#line:709
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('sucv')#line:710
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:711
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:712
        elif O00O0O000O0OO0O00 .get ("proc")=='Act4ftMiner':#line:713
            _OO0O0OO0000O0OOOO =O00O0O000O0OO0O00 .get ("cond")#line:716
            if _OO0O0OO0000O0OOOO !=None :#line:717
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:718
            else :#line:719
                O00O0O000O0OO000O =OOOOOOO0OO00O0OO0 .cedent #line:720
                O00O0O000O0OO000O ['cedent_type']='cond'#line:721
                O00O0O000O0OO000O ['filter_value']=(1 <<OOOOOOO0OO00O0OO0 .data ["rows_count"])-1 #line:722
                O00O0O000O0OO000O ['generated_string']='---'#line:723
                print (O00O0O000O0OO000O ['filter_value'])#line:724
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:725
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents'].append (O00O0O000O0OO000O )#line:726
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('antv-')#line:727
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('antv+')#line:728
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:729
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:730
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:731
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:732
        elif O00O0O000O0OO0O00 .get ("proc")=='SD4ftMiner':#line:733
            _OO0O0OO0000O0OOOO =O00O0O000O0OO0O00 .get ("cond")#line:736
            if _OO0O0OO0000O0OOOO !=None :#line:737
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:738
            else :#line:739
                O00O0O000O0OO000O =OOOOOOO0OO00O0OO0 .cedent #line:740
                O00O0O000O0OO000O ['cedent_type']='cond'#line:741
                O00O0O000O0OO000O ['filter_value']=(1 <<OOOOOOO0OO00O0OO0 .data ["rows_count"])-1 #line:742
                O00O0O000O0OO000O ['generated_string']='---'#line:743
                print (O00O0O000O0OO000O ['filter_value'])#line:744
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('cond')#line:745
                OOOOOOO0OO00O0OO0 .task_actinfo ['cedents'].append (O00O0O000O0OO000O )#line:746
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('frst')#line:747
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('scnd')#line:748
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('ante')#line:749
            OOOOOOO0OO00O0OO0 .task_actinfo ['cedents_to_do'].append ('succ')#line:750
        else :#line:751
            print ("Unsupported procedure")#line:752
            return #line:753
        print ("Will go for ",O00O0O000O0OO0O00 .get ("proc"))#line:754
        print ("Starting to mine rules.")#line:761
        OOOOOOO0OO00O0OO0 ._start_cedent (OOOOOOO0OO00O0OO0 .task_actinfo )#line:762
        OOOOOOO0OO00O0OO0 .stats ['end_proc_time']=time .time ()#line:764
        print ("Done. Total verifications : "+str (OOOOOOO0OO00O0OO0 .stats ['total_cnt'])+", hypotheses "+str (OOOOOOO0OO00O0OO0 .stats ['total_valid'])+",control number:"+str (OOOOOOO0OO00O0OO0 .stats ['control_number'])+", times: prep "+str (OOOOOOO0OO00O0OO0 .stats ['end_prep_time']-OOOOOOO0OO00O0OO0 .stats ['start_prep_time'])+", processing "+str (OOOOOOO0OO00O0OO0 .stats ['end_proc_time']-OOOOOOO0OO00O0OO0 .stats ['start_proc_time']))#line:767
        O0OOO00OOOO0O00O0 ={}#line:768
        OO0O0O0000OOO00OO ={}#line:769
        OO0O0O0000OOO00OO ["task_type"]=O00O0O000O0OO0O00 .get ('proc')#line:770
        OO0O0O0000OOO00OO ["target"]=O00O0O000O0OO0O00 .get ('target')#line:772
        OO0O0O0000OOO00OO ["self.quantifiers"]=OOOOOOO0OO00O0OO0 .quantifiers #line:773
        if O00O0O000O0OO0O00 .get ('cond')!=None :#line:775
            OO0O0O0000OOO00OO ['cond']=O00O0O000O0OO0O00 .get ('cond')#line:776
        if O00O0O000O0OO0O00 .get ('ante')!=None :#line:777
            OO0O0O0000OOO00OO ['ante']=O00O0O000O0OO0O00 .get ('ante')#line:778
        if O00O0O000O0OO0O00 .get ('succ')!=None :#line:779
            OO0O0O0000OOO00OO ['succ']=O00O0O000O0OO0O00 .get ('succ')#line:780
        O0OOO00OOOO0O00O0 ["taskinfo"]=OO0O0O0000OOO00OO #line:781
        OOO0O0O0000000O00 ={}#line:782
        OOO0O0O0000000O00 ["total_verifications"]=OOOOOOO0OO00O0OO0 .stats ['total_cnt']#line:783
        OOO0O0O0000000O00 ["valid_hypotheses"]=OOOOOOO0OO00O0OO0 .stats ['total_valid']#line:784
        OOO0O0O0000000O00 ["time_prep"]=OOOOOOO0OO00O0OO0 .stats ['end_prep_time']-OOOOOOO0OO00O0OO0 .stats ['start_prep_time']#line:785
        OOO0O0O0000000O00 ["time_processing"]=OOOOOOO0OO00O0OO0 .stats ['end_proc_time']-OOOOOOO0OO00O0OO0 .stats ['start_proc_time']#line:786
        OOO0O0O0000000O00 ["time_total"]=OOOOOOO0OO00O0OO0 .stats ['end_prep_time']-OOOOOOO0OO00O0OO0 .stats ['start_prep_time']+OOOOOOO0OO00O0OO0 .stats ['end_proc_time']-OOOOOOO0OO00O0OO0 .stats ['start_proc_time']#line:787
        O0OOO00OOOO0O00O0 ["summary_statistics"]=OOO0O0O0000000O00 #line:788
        O0OOO00OOOO0O00O0 ["hypotheses"]=OOOOOOO0OO00O0OO0 .hypolist #line:789
        OOO0O00000OOO00O0 ={}#line:790
        OOO0O00000OOO00O0 ["varname"]=OOOOOOO0OO00O0OO0 .data ["varname"]#line:791
        OOO0O00000OOO00O0 ["catnames"]=OOOOOOO0OO00O0OO0 .data ["catnames"]#line:792
        O0OOO00OOOO0O00O0 ["datalabels"]=OOO0O00000OOO00O0 #line:793
        OOOOOOO0OO00O0OO0 .result =O0OOO00OOOO0O00O0 #line:795

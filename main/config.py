class Config:
    correction = False
    # Для файлов Levenhuk
    thresholdWindow = 71
    thresholdConst = 8
    scale = 0.0281
    closureConst = 3
    files_list = [['one_1.png', 'one_2.png', 'one_3.png'],
                  ['two_1.png', 'two_2.png', 'two_3.png'],
                  ['three_1.png', 'three_2.png', 'three_3.png']]

    # Для файлов с БиОптик
    # thresholdWindow = 251
    # thresholdConst = 8
    # scale = 0.007036
    # closureConst = 15
    # files_list = [['my_1_1.png', 'my_1_2.png', 'my_1_3.png'],
    #                  ['my_2_1.png', 'my_2_2.png', 'my_2_3.png'],
    #                  ['my_3_1.png', 'my_3_2.png', 'my_3_3.png']]

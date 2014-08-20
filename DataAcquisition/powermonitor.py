from data_point  import data_point


vrms=data_point(
  dict_point={

        'Tag':'CTSVRMS01',
        'Desc':'１号传感器电压有效值',
        'EngUnit':'V',
        'PointSource':'S',
        'PointType':'FLOAT32',
        'Zero':'220',
        'Exception_max':290,
        'Exception_min':190
  })

irms=data_point(
  dict_point={

        'Tag':'CTSIRMS01',
        'Desc':'１号传感器电流有效值',
        'EngUnit':'A',
        'PointSource':'S',
        'PointType':'FLOAT32',
        'Zero':'0',
        'Exception_max':10,
        'Exception_min':0
  })

irms=data_point(
  dict_point={

        'Tag':'CTSIRMS01',
        'Desc':'１号传感器电流有效值',
        'EngUnit':'A',
        'PointSource':'S',
        'PointType':'FLOAT32',
        'Zero':'0',
        'Exception_max':10,
        'Exception_min':0
  })

rpower=data_point(
  dict_point={

        'Tag':'CTSRP01',
        'Desc':'１号传感器有用功',
        'EngUnit':'W',
        'PointSource':'S',
        'PointType':'FLOAT32',
        'Zero':'0',
        'Exception_max':1000,
        'Exception_min':0
  })
apower=data_point(
  dict_point={

        'Tag':'CTSAP01',
        'Desc':'１号传感器视在功',
        'EngUnit':'VA',
        'PointSource':'S',
        'PointType':'FLOAT32',
        'Zero':'0',
        'Exception_max':1000,
        'Exception_min':0
  })
pf=data_point(
  dict_point={

        'Tag':'CTSPF01',
        'Desc':'１号传感器功率因数',
        'EngUnit':'',
        'PointSource':'S',
        'PointType':'FLOAT32',
        'Zero':'0.5',
        'Exception_max':1,
        'Exception_min':0
  })






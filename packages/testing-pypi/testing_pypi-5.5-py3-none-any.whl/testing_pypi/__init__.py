#__init__.py
"""Testing fire"""
# def helloWorld():
#    print("Hello World I hope this works!")
   
# import fire

#Pipeline class calls the other classes methods called run and then we just need to call one class
#$ python example.py ingestion run or $ python example.py digestion run
# class IngestionStage_(object):

#   def run(self):
#     print('here_ingestion')
#     return 'Ingesting! Nhom nhom nhom...'
    
# class DigestionStage(object):

#   def run(self, volume=1):
#     print('here_digestion')
#     return ' '.join(['Burp!'] * volume)

#   def status(self):
#     return 'Satiated.'

# class Pipeline(object):

#   def __init__(self):
#     self.ingestion = IngestionStage_()
#     self.digestion = DigestionStage()
#     print('here_init')

#   def run(self):
#     self.ingestion.run()
#     self.digestion.run(2)
#     print('here_method_pipeline')

# if __name__ == '__main__':
#   fire.Fire(Pipeline)



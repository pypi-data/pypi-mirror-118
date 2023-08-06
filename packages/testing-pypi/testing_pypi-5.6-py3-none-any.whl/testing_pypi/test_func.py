# def retorna3():
#   return 3

# def test_retorna31():
#   assert retorna3() == 3

# #v4 calling a object $python ex_fire.py add 10 10
# import fire
# class Calculator(object):

#   def add(self, x=1, y=2): #$python test_func.py calc add --x 3 --y 6 ou 
#     return x + y

#   def multiply(self, x, y): #python test_func.py calc multiply 10 10
#     return x * y

# class Pipeline(object):
#   def __init__(self):
#     self.retorna = retorna3
#     self.calculator = Calculator()

# if __name__ == '__main__':
#   fire.Fire(Pipeline)

def retorna3():
  return 3

def test_retorna31():
  assert retorna3() == 3

#v4 calling a object $python ex_fire.py add 10 10
import fire
class Calculator(object):

  def add(self, x=1, y=2): #$python test_func.py calc add --x 3 --y 6 ou 
    return x + y

  def multiply(self, x, y): #python test_func.py calc multiply 10 10
    return x * y

class Pipeline(object):
  def __init__(self):
    self.retorna = retorna3
    self.calculator = Calculator()

if __name__ == '__main__':
  fire.Fire(Pipeline)
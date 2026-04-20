class AreaConvert():
    def __init__(self):
          self.areaD = {}
          self.areaD['sqmeter']      = 1.0
          self.areaD['sqmillimeter'] = 1000000.0
          self.areaD['sqcentimeter'] = 10000.0
          self.areaD['sqkilometer']  = 0.000001
          self.areaD['hectare']      = 0.0001
          self.areaD['sqinch']       = 1550.003
          self.areaD['sqfoot']       = 10.76391
          self.areaD['sqyard']       = 1.19599
          self.areaD['acre']         = 0.0002471054
          self.areaD['sqmile']       = 0.0000003861022
          self.areaD['Ha']           = 0.0001
          self.areaD['a']            = 0.01
          self.areaD['Ca']           = 1
          self.Area = {}
          self.Area['Ha'] = 0
          self.Area['a'] = 0
          self.Area['Ca'] = 0
          self.Ha = 0
          self.a = 0
          self.Ca = 0

    def convertArea(self,x, unit1 = None, unit2 = None): # Mamadika metre carre en Ha a Ca
        self.Ha_d = x / 10000 #valeur en Ha avec decimale
        self.Ha = x // 10000
        temp = x - (self.Ha * 10000)
        self.a = temp // 100
        self.Ca = temp - (self.a * 100)
        self.Ca = round(self.Ca, 2)
        self.Area['Ha'] = self.Ha
        self.Area['a'] = self.a
        self.Area['Ca'] = self.Ca
        self.Area['Ha_d'] = self.Ha_d
        return self.Area

    def convertAreaToHa(self, x, unit1 = None, unit2 = None):
        self.Ha_d = x / 10000
        return round(self.Ha_d, 4)

    def convertAreaToA(self, x, unit1 = None, unit2 = None):
        self.a = x / 100
        return round(self.a, 4)
#  def convertArea(self,x, unit1, unit2):
#      if (unit1 in self.areaD) and (unit2 in self.areaD):
#          factor1 = self.areaD[unit1]
#          factor2 = self.areaD[unit2]
#          self.Ha = (factor2*x//factor1)
#          if self.Ha >= 1 :
#              temp = factor2 * x
#              resteAre = (temp % factor1)
 #             number_dec = str(resteAre - int(resteAre))[2:]
#              fare1 = self.areaD['sqmeter']
 #             fare2 = self.areaD['a']
#              self.a = (fare2 * int(number_dec) // fare1)
  #           resteCa = (fare2 * int(number_dec) % fare1)
 #         else :
  #            self.Ha = 0
   #           factor1 = self.areaD['sqmeter']
    #          factor2 = self.areaD['a']
     #         self.a = (factor2 * x // factor1)
      #        temp = factor2 * x
       #       resteAre = (temp % factor1)
        #      number_dec = str(resteAre - int(resteAre))[2:]
         #     fCa1 = self.areaD['sqmeter']
          #    fCa2 = self.areaD['Ca']
         #     print "resteAre"
          #    print resteAre
          #    resteCa = number_dec


#        print str(Ha)+"Ha "+str(a)+"a "+str(resteCa)+"Ca"
       #   self.Area['a']  = self.a
       #   self.Area['Ca'] = resteCa
       #   self.Area['Ha'] = self.Ha
       #   print self.Area
       #   return  self.Area
#        return round(factor2*x/factor1,0)
     # else:
         # return False

# test1: x square-miles have how many acres?
x = 1989.2
unit1 = 'sqmeter'
unit2 = 'Ha'
a  = 9
b  = 2
y = 0.69982
print (y%100)
#print "a mod b"
AC  = AreaConvert()
outcome = AC.convertArea(x, unit1, unit2)
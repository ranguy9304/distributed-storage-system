from settings import *
import json
import pickle



class PacketClass:
    type = None
    msg = None
    def __init__(self,type=None,msg=None):
        self.type=type
        self.msg=msg

class Data:
	attributes = ""
	desc = ""
	def __init__(self,atr,desc):
		self.attributes=atr
		self.desc=desc

	def getJson(self):
		return json.dumps(self.__dict__)

	


class JsonPacket:
	type=None
	msg=None
	def __init__(self,data=None):
		if data != None:
			rcvmsg =pickle.loads(data)
			if rcvmsg.type :
				self.type=rcvmsg.type
				if self.type==POST :
					self.msg=json.loads(rcvmsg.msg)
				elif self.type==FETCH_RESP :
					self.msg = pickle.loads(rcvmsg.msg)
	@staticmethod
	def POSTPacket(data):
		ret = JsonPacket()
		ret.type=POST
		ret.msg=data.getJson()
		return pickle.dumps(ret)
	@staticmethod
	def FETCHPacket(data = None):
		ret = JsonPacket()
		ret.type=FETCH

		ret.msg=data.getJson() if data !=  None else None
		return pickle.dumps(ret)
	@staticmethod
	def FETCH_RESPPacket(data):
		ret = JsonPacket()
		ret.type=FETCH_RESP
		ret.msg=pickle.dumps(data)
		return pickle.dumps(ret)
	def __str__(self):
		# if self.type == FETCH_RESP:
		# 	return self.type + " " + str(pickle.loads(self.msg))
		# else:
		return self.type + " " + str(self.msg)
	def getJson(self):
		return json.dumps(self.__dict__)
	def toJSON(self):
		return json.dumps(self.__dict__)


	



import os
import redis
from elasticsearch import Elasticsearch
import json

ES = Elasticsearch(host=os.environ['ELASTIC_IP'], port=os.environ['ELASTIC_PORT'])
r = redis.StrictRedis(host=os.environ['REDIS_IP'], port=os.environ['REDIS_PORT'], db=1)

def set_value(key,value):
	print key
	pipe = r.pipeline()
	pipe.set(key,value)
	pipe.execute()


def create_nurl(host):

	"""
		call to update nurl of the dump on the basis of _id field
		eg:
			host = "http://myadserver.com"
			_id = "qwerty" (elasticsearch _id)
			url = "http://myadserver.com/?id=qwerty"
	"""

	req_body = {
		"fields":[],
		"size":300
	}
	res = ES.search(index=os.environ["ELASTIC_INDEX"],doc_type=os.environ["ELASTIC_TYPE"],body=req_body)
	for result in res["hits"]["hits"]:
		print result
		key = result["_id"]
		url = host+"/?id="+key+"&price=${AUCTION_PRICE}"
		print key,url
		res = ES.update(index=os.environ["ELASTIC_INDEX"],doc_type=os.environ["ELASTIC_TYPE"],id=key,
                body=json.dumps({"doc": {"nurl": url }}))


def create_ad_markup():
	"""
		call to create ad markup with proper format, height and width fields encoded
	"""
	req_body = {
		"size":300
	}
	res = ES.search(index=os.environ["ELASTIC_INDEX"],doc_type=os.environ["ELASTIC_TYPE"],body=req_body)
	for result in res["hits"]["hits"]:
		print result
		key = result["_id"]
		height = result["_source"]["height"]
		width = result["_source"]["width"]
		ad_markup = "<?xml version='1.0' encoding='ISO-8859-1'?><ad modelVersion='0.9'><imageAd><clickUrl>http://mysite.com/landingpages/mypage/</clickUrl><imgUrl>http://mysite.com/images/myad.jpg</imgUrl><width>"+str(width)+"</width><height>"+str(height)+"</height><toolTip>This is a tooltip text</toolTip><additionalText>Additional text to be displayed</additionalText><beacons><beacon>http://mysite.com/beacons/mybeacon1</beacon><beacon>http://mysite.com/beacons/mybeacon2</beacon></beacons></imageAd></ad>"
		res = ES.update(index=os.environ["ELASTIC_INDEX"],doc_type=os.environ["ELASTIC_TYPE"],id=key,
        body=json.dumps({"doc": {"adm": ad_markup }}))

def set_bid_price():
	req_body = {
		"size":300
	}
	res = ES.search(index=os.environ["ELASTIC_INDEX"],doc_type=os.environ["ELASTIC_TYPE"],body=req_body)
	for result in res["hits"]["hits"]:
		print result
		key = result["_id"]
		res = ES.update(index=os.environ["ELASTIC_INDEX"],doc_type=os.environ["ELASTIC_TYPE"],id=key,
                body=json.dumps({"doc": {"bid_amount": 0.5 }}))

def generate_dump():
	
	"""
		call to generate default key value pairs in redis
		key is elasticsearch id
		value is the max amount of times the bid can happen ie budget/bid_amount
	"""

	req_body = {
		"fields":["bid_amount","budget"],
			"size": 300
	}
	res = ES.search(index=os.environ["ELASTIC_INDEX"],doc_type=os.environ["ELASTIC_TYPE"],body=req_body)
	for result in res["hits"]["hits"]:
		print result
		key = result["_id"]
		bid_amount = result["fields"]["bid_amount"][0]
		budget = result["fields"]["budget"][0]
		value = int(budget)
		print key,bid_amount,budget,value
		set_value(key,value)


if __name__ == "__main__":
	generate_dump()
	#create_nurl("http://128.199.206.102:8080")
	#create_ad_markup()
	#set_bid_price()
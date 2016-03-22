from ..settings import ES,r
from ..models import global_counters
import json
import os
from main import celery_app

def change_value(key,value):
    with r.pipeline() as pipe:
        while 1:
            try:
                pipe.watch(key)
                current_value = pipe.get(key)
                next_value = float(current_value)-float(value)
                pipe.multi()
                pipe.set(key,next_value)
                pipe.execute()
                break
            # except WatchError:
            #     continue
            except Exception,e:
                print str(e)
                continue
            finally:
                pipe.reset()

def get_value(key):
    with r.pipeline() as pipe:
        while 1:
            try:
                pipe.watch(key)
                current_value = pipe.get(key)
                break
            # except WatchError:
            #     continue
            except Exception,e:
                print str(e)
                continue
            finally:
                pipe.reset()
                return float(current_value)

@celery_app.task()
def query_elastic(key):
	try:
		res = ES.update(index=os.environ["ELASTIC_INDEX"],doc_type=os.environ["ELASTIC_TYPE"],id=key,
                body=json.dumps({"doc": {"is_active": False }}))
	except Exception,e:
		print str(e)

def update_win_price(key):
    try:
        req_body = {
            "fields":["bid_amount"],
            "query":{
                "match":{
                  "_id": key
                }
              }
            }
        res = ES.search(index=os.environ["ELASTIC_INDEX"],doc_type=os.environ["ELASTIC_TYPE"],body=req_body)
        return res["hits"]["hits"][0]["fields"]["bid_amount"][0]
    except Exception,e:
        print str(e)


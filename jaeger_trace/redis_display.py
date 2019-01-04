from flask import Flask
from flask import request
import redis
from tracer import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format
import json
import requests
import os


app = Flask(__name__)
tracer = init_tracer('redis-display')
redis_host = str(os.getenv('REDIS_HOST'))
#redis_port = str(os.getenv('REDIS_PORT'))
init_redis = redis.StrictRedis(host=redis_host, port=6379, db=0)


@app.route('/display')
def display_values():
	
	span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
	span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

	with tracer.start_active_span('redis-display-span', child_of=span_ctx, tags=span_tags):
		print(type(conn_redis.get('Delivery-Guy')))
		print(type(conn_redis.get('item_ordered')))
		return "hello world"


# request for stored information
@app.route('/order-info')
def get_order_info():
	delivery_guy = requests.args.get('Delivery')
	retv_details = redis.get('delivery_guy')

	return retv_details
	


if __name__ == '__main__':

	app.run(port=8083)

from flask import Flask
from flask import request
import redis
from tracer import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format
import json
import requests
import os
from flask import jsonify




app = Flask(__name__)
tracer = init_tracer('redis-display')
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', '6379')

conn_redis = redis.StrictRedis(host=redis_host, port=int(redis_port), db=0)
#conn_redis = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.route('/display')
def display_values():
	span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
	span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
	with tracer.start_active_span('redis-display-span', child_of=span_ctx, tags=span_tags):
	#with tracer.start_span('redis-display-span', child_of=span_ctx, tags=span_tags):
		
		delv_guy = conn_redis.get('Delivery_Guy')
		order_item = conn_redis.get('Order-Item')
		order_id = request.headers.get('Order-Id')
		
		order_info = {'Order-Id': order_id,
						'Delivery_Guy': delv_guy.decode('utf-8'),
						'Order-Item': order_item.decode('utf-8')}
		print(order_info)
		#dupe_list=[i.decode('utf-8') for i in key_list]

		return jsonify(order_info)
# # request for stored information
# @app.route('/order-info')
# def get_order_info():
# 	delivery_guy = requests.args.get('Delivery')
# 	retv_details = redis.get('delivery_guy')

# 	return retv_details
	


if __name__ == '__main__':

	app.run(host='0.0.0.0', port=8083)

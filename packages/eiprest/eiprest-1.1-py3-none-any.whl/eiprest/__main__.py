import argparse
import json
from .eiprest import EipRest

parser = argparse.ArgumentParser(prog='python -m eiprest')
parser.add_argument('-d', '--debug', help='enable debug mode', action='store_true')
parser.add_argument('-s', '--server', help='Solidserver hostname or IP address', required=True)
parser.add_argument('-u', '--user', default='ipmadmin', help="Solidserver username ('ipmadmin' by default)")
parser.add_argument('-p', '--password', default='admin', help="User password ('admin' by default)")
parser.add_argument('-m', '--method', help='HTTP method', default='GET', choices=['GET','POST','PUT','DELETE','OPTIONS'])
parser.add_argument('-r', '--rpc', help='use RPC API instead of REST API', action='store_true')
parser.add_argument('-f', '--filters', help='filter output parameters')
parser.add_argument('--where', help='WHERE parameter of the service')
parser.add_argument('service', help='service to run')
parser.add_argument('parameters', help='paramters of the service', nargs='?')
args = parser.parse_args()

rest = EipRest(args.server, args.user, args.password, args.debug, args.filters)
param = rest.param2dict(args.parameters)
if args.where:
  param.update({'WHERE': args.where})
        
print("===========================")
if args.rpc:
  print(f"RPC: {args.method} {args.service} {json.dumps(param)}")
  rest.rpc(args.method, args.service, param)
else:
  print(f"REST: {args.method} {args.service} {json.dumps(param)}")
  rest.query(args.method, args.service, param)

rest.show_result()

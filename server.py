#!/usr/bin/python3

import time
import json
import SimpleHTTPServer 
import SocketServer
from io import BytesIO

import gspread
import google_io as scoreSheets
import sys

HOST_NAME = 'localhost'
PORT_NUMBER = 85


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_HEAD(self):
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

    def do_GET(self):
      self.send_response(200)
    
    def do_POST(self):
      content_length = int(self.headers['Content-Length'])
      body = self.rfile.read(content_length)
      self.send_response(200)
      self.end_headers()

      try:
        fulfillmentJson = json.loads(body.decode('ascii'))
        print(json.dumps(fulfillmentJson, sort_keys=False, indent=4))
        query = fulfillmentJson["queryResult"]
        intent = query["intent"]["displayName"]
        params = query["parameters"]
        

        if intent == "Start score keeper":
          print("The email to use is : " + str(params["sheetemail"]))
          scoreSheets.new_game(params["sheetemail"])
          scoreSheets.add_players(params["playernames"])

        elif intent == "addScore":
          print("Adding %d to %s" % (int(params["points"]), params["playername"]))
          scoreSheets.update_score(params["playername"], params["points"])

        elif intent == "getScore":
          print("Need to get a player's score")

        elif intent == "clearRound":
          print("Clearing round")
          scoreSheets.clear_scores()

        elif intent == "addPlayer":
          print("Adding new player")
          scoreSheets.add_players([params["playername"]])

        elif intent == "nextRound":
          print("Next round")
          scoreSheets.new_round()

        elif intent == "getLeader":
          print("Getting Leader")
          leader = scoreSheets.get_leader()
          print("Leader is : %s" % (leader,))
          resp = "{\"messages\": [{\"speech\": \"%s is currently in the lead right now\",\"type\": 0}]}" % (leader,)
          print(resp)
          jsonResp = json.loads(resp)
          print(str(jsonResp))
          self.wfile.write(bytes(jsonResp))   

        else:
          print("Uknown intent met: " + str(intent))

      except gspread.exceptions.APIError as e:
        print("Found api error")
        print(str(e))
      except :
        print("Uknown POST Request encountered")
        print("Error: ", sys.exc_info()[0])


    def handle_http(self, status_code, path):
      self.send_response(status_code)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      content = '''
      <html><head><title>Title goes here.</title></head>
      <body><p>This is a test.</p>
      <p>You accessed path: {}</p>
      </body></html>
      '''.format(path)
      return bytes(content, 'UTF-8')

    def respond(self, opts):
      response = self.handle_http(opts['status'], self.path)
      self.wfile.write(response)

if __name__ == '__main__':
    httpd = SocketServer.TCPServer(("", PORT_NUMBER), MyHandler) 
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
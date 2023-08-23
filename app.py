
import json

from flask import Flask, jsonify, request
from datetime import datetime
from datetime import date
app = Flask(__name__)

# Load data from the JSON file
with open('data.json', 'r',encoding='utf-8') as file:
    data = json.load(file)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/search', methods=['GET'])
def search():
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    final_data=[]

    def rem_time(d):
        s = datetime(d.year,d.month, d.day)
        return s
    if at_from:
            if type(at_from)== datetime:
                pass
            else:
                try:
                    at_from = datetime.strptime(at_from, "%d-%b-%Y")
                except ValueError or TypeError:
                    try:
                        at_from = datetime.strptime(at_from, "%d-%m-%Y")
                    except ValueError:
                        pass
    else:
        None   
        
    if at_to:
            if type(at_to)==datetime :
                pass
            else:
                try:
                    at_to = datetime.strptime(at_to, "%d %b %y")
                except ValueError:
                    try:
                        at_to = datetime.strptime(at_to, "%d-%m-%Y")
                    except ValueError:
                        pass        
    else:
        None                
    for item in data:
        
        match_author= search_author is None or (search_author.lower() in item["author"].lower())
        
        if type(item["at"])== datetime:
            item["at"]=rem_time(item["at"])
        else :   
            # print(type(item["at"]))
            item["at"]= datetime.strptime(item["at"] , "%a, %d %b %Y %H:%M:%S %Z" )
            item["at"]=rem_time(item["at"])
     
        
        match_at_from= at_from is None or item["at"] >= at_from
       
        match_at_to= at_to is None or item["at"] <= at_to
        match_like_from= like_from is None or item["like"] >= int(like_from)
        match_like_to= like_to is None or item["like"] <= int(like_to)
        match_reply_from= reply_from is None or item["reply"] >= int(reply_from)
        match_reply_to= reply_to is None or item["reply"] <= int(reply_to)
        match_search_text= search_text is None or ( search_text in item["text"] )

        if match_author and match_at_from and match_at_to and match_like_from and match_like_to and match_reply_from and  match_reply_to and match_search_text:
            final_data.append(item)
      
    if not final_data:
        return jsonify({"message":"No items found for the given search parameters"}), 404

    return jsonify(final_data)        

@app.route('/')
def hello_world():
    return 'Hello, World!'





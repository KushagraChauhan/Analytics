from flask import Flask, request, jsonify, render_template,session,jsonify
import json
import requests

app = Flask(__name__)

@app.route('/get_unprocessedfile',methods=['POST','GET'])
def get_unprocessedfile():

    url = request.args['url']
    print(url)
    # url = data['url']
    print("file bot 0")
    client_id = request.args['client_id']
    r = requests.get(url)
    data = r.json()
    urls = []
    file_name = []
    download_url = []
    #here I have to write get_domain function
    print("file bot 1")
    try:
        for iter in data['data']:
            temp_url = "http://test.techeela.net/" + iter
            urls.append(temp_url)
            temp_download_url = "http://test.techeela.net/api/"+iter
            download_url.append(temp_download_url)
            iter = iter.split('/')
            file_name.append((''.join([i for i in iter[len(iter)-1] if not i.isdigit()])).replace('-',''))
        print("request sent")
        data['urls'] = urls
        data['file_name'] = file_name
        data['download_url'] = download_url
        # print("############-  ",data['urls'])
        print("data --> ",data)
        return jsonify({"data":data,"domain":"http://test.techeela.net"})
    except Exception as e:
        print("NO File")
        return jsonify({"data":data,"domain":"http://test.techeela.net"})


if __name__ == "__main__":
    app.run(debug=True)

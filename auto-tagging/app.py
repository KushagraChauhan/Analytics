'''
######################################
Issue #1000- Auto Tagging of files
######################################
'''
import RAKE
from rake_nltk import Rake,  Metric
from tika import parser
import requests
from requests import Session
from urllib.parse import urlparse
from os.path import splitext
from flask import Flask, request, jsonify, render_template,session,jsonify

app = Flask(__name__)
@app.route('/auto-tagger' ,methods=['POST','GET'])
def auto():
    email = request.args['email']
    password = request.args['password']
    url = request.args['url']
    payload = {'email':email,'password':password}

    with Session():
        session = requests.Session()
        response = session.post('https://gateway.eela.tech/api/login',data=payload)
        x = response.text
        y = x.strip('{}')
        z = y.strip('"success":{"token":')
        token = z.strip('","app":"1234560')

        token_final = '"'+"Bearer "+token+'"'
        headers = {"Authorization": token_final}
        #file_url = "https://thp.techeela.net/api/knowledgemanager/files/shares/Techeela%20Custom%20API%20documentation.docx"
        path = urlparse(url).path
        ext = splitext(path)[1]
        r = requests.get(url, headers=headers,verify=False,stream=True)
        r.raw.decode_content = True
        print("hello")
        if ext == ".pdf":
            with open("/tmp/1.pdf","wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                     # writing one chunk at a time to pdf file
                     if chunk:
                         pdf.write(chunk)

                raw = parser.from_file('/tmp/1.pdf')
                r = Rake(ranking_metric=Metric.WORD_FREQUENCY, max_length=1)
                text = raw['content']
                r.extract_keywords_from_text(text)
                key = r.get_ranked_phrases()
                tags = []
                for i in range(10):
                    print("Keywords:", key[i])
                    tags.append(key[i])

                return jsonify(tags)

        if ext == ".docx":
            with open("/tmp/1.docx","wb") as doc:
                for chunk in r.iter_content(chunk_size=1024):
                     # writing one chunk at a time to doc file
                     if chunk:
                         doc.write(chunk)

            raw = parser.from_file('/tmp/1.docx')
            r = Rake(ranking_metric=Metric.WORD_FREQUENCY, max_length=1)
            text = raw['content']
            r.extract_keywords_from_text(text)
            key = r.get_ranked_phrases()
            tags = []
            for i in range(10):
                print("Keywords:", key[i])
                tags.append(key[i])

            return jsonify(tags)



if __name__ == "__main__":
    app.run(debug=True)

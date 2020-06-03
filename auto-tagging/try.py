import requests
from requests import Session
payload = {'email':'vikram.singh@forethought.in','password':'123456'}

with Session():
    session = requests.Session()
    response = session.post('https://gateway.eela.tech/api/login',data=payload)
    x = response.text
    y = x.strip('{}')
    z = y.strip('"success":{"token":')
    token = z.strip('","app":"1234560')

    token_final = '"'+"Bearer "+token+'"'
    headers = {"Authorization": token_final}
    file_url = "https://thp.techeela.net/api/knowledgemanager/files/shares/Company/User%20Management%20UC%20Diagram.pdf"
    r = requests.get(file_url, headers=headers,verify=False,stream=True)
    r.raw.decode_content = True
    with open("1.pdf","wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
             # writing one chunk at a time to pdf file
             if chunk:
                 pdf.write(chunk)

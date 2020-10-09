from flask import Flask,render_template,request
import whois
from datetime import datetime
# from google.cloud import firestore
# from google.cloud import storage
import requests


app = Flask(__name__)



def queryDomain(url):
  domain={}
  w = whois.whois(url)
  if w["domain_name"]==None:
      return 'Invalid domain name'
  if type(w["domain_name"])== list:
      domain_name= w["domain_name"][0]
  else:
      domain_name = w["domain_name"]
  domain['Domain Name']=domain_name
  if type(w["expiration_date"])== list:
      domain["Expires on"]= w["expiration_date"][0]
  else:
      domain["Expires on"] = w["expiration_date"]
  if type(w["creation_date"])== list:
      domain["Created on"]= w["creation_date"][0]
  else:
      domain["Created on"] = w["creation_date"]
  domain["Belongs to"]=w["org"]
  domain["State"]=w["state"]
  domain["Country"]=w["country"]
  domain["Registrar"]=w["registrar"]
  
  domain["Expires on"]=domain["Expires on"].strftime("%B %m %Y at %H:%M %p")
  domain["Created on"]=domain["Created on"].strftime("%B %m %Y at %H:%M %p")
  domain["imageurl"]='https://www.'+domain_name+'/favicon.ico'


  # try:
  #   url='http://'+domain_name+'/favicon.ico'
  #   r = requests.get(url, allow_redirects=True)
  #   if r.status_code==200:
  #       filename='/tmp/'+domain_name+'.png'
  #       open(filename, 'wb').write(r.content)

  #       storage_client = storage.Client()
  #       bucket = storage_client.bucket('favicon')
  #       blob = bucket.blob(domain_name)
  #       blob.upload_from_filename(filename)
  #       domain["imageurl"]='https://storage.googleapis.com/resize-favicon/'+domain_name

  # except Exception as e:
  #     print(Exception)

#   db=firestore.Client()
#   db.collection('domain').document(domain_name).set(domain)

  return domain

# def allDomain():
#   alldomains=[]
#   db = firestore.Client()
#   domains = db.collection('domain').stream()
#   for d in domains:
#     alldomains.append(d.to_dict())
#   return alldomains


@app.route('/')
def home():
  return render_template('index.html')

@app.route('/domaindetails',methods = ['POST'])
def details():
  url=request.form['url']
  result=queryDomain(url)
  return render_template('domaindetails.html',result=result)

# @app.route('/alldomains',methods = ['GET'])
# def listdomain():
#   result=allDomain()
#   return render_template('alldomains.html',result=result)

if __name__ == '__main__':
  app.run(host='0.0.0.0')
  #app.run()

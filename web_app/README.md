# run the ui
- all of the following commands must be run from the 'web' directory
- Installs the vue cli 
```
npm install -g @vue/cli
```
- install the node packages
```
npm install
```
- run the development server
```
npm start
```
- view the page
http://localhost:8081

# run the server

- build the app and put the output in the API directory (run from 'web' directory)
```
npm run build
```
- install the requirements
```
pip install -r requirements.txt
```
- run the flask server
```
python main.py
```
  
- http://localhost:8080/api/ui
- http://localhost:8080

# build and run the docker image
```
docker-compose up --build
```
- http://localhost:8080

# deploy the app
- requires the aws cli and the fargate cli (https://somanymachines.com/fargate/)
- ask me for some credentials to my AWS account
```
sh deploy.sh
```

- http://ec2co-ecsel-1w78movq5gw2-1222388112.us-east-1.elb.amazonaws.com/
- http://ec2co-ecsel-1w78movq5gw2-1222388112.us-east-1.elb.amazonaws.com/api/ui
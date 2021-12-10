Prerequisites

Python 3
Node v16+

Steps to run

Create a virtual environment.
Activate the virtual environment.
Run pip install -r requirements.txt
Download models from below link. 
Run flask run to run backend server.
Run yarn start to start frontend server.

Important Links

link to models. (https://drive.google.com/drive/folders/1od_OnApLLPATjolhaLYr5tQvZHtA2U0U?usp=sharing)

Setup

To test on your clip
For now, simply pass in the url of the video to the predict_video function inside server.py
We are in the process of adding this feature in to our frontend.

To store the timestamps on Mongo
Simply edit the connection string in server.py

What’s left?
 Create an overall model for all events, currently we have single models for each event
 Change code in backend to appropriately store timestamps for overall model
 Create the upload video pipeline.
 Host the webapp.
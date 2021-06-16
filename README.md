##NTHU 2018 Spring Semester Data Science Final Project

### Goal
* Using LSTM based on Keras to predict whether the comment in the article is useful

### Step
* Crawl the articles from 2018.1 to 2018.3 in [PTT Gossiping](https://www.ptt.cc/bbs/Gossiping/index.html)
* Design a GUI for labeling some comment data
* Using the library ['Jieba'](https://github.com/fxsjy/jieba) to segement all dataset
* Divide all data into three parts including training, validate, and testing data
* Construce a LSTM model by using training data
* Using testing data to evalute the model

### Result 
Given a URL from PTT Gossiping, it generates a new HTML file. In the new HTML, it changes the color of the useless comments. We give each user who is in our dataset a credit score. Finally, we also judge whether the article is shit posting, if yes, it will be given a "Shitposting Mark.

![result](https://github.com/ZTingLiu/Data-Science-Project/blob/master/img/comment.png?raw=true)

![result](https://github.com/ZTingLiu/Data-Science-Project/blob/master/img/shitposting.png?raw=true)

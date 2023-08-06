#!/usr/bin/env python
# coding: utf-8

# # 疫情期间网民情绪识别   
# 数据简介: 数据集依据与“新冠肺炎”相关的230个主题关键词进行数据采集，   
# 抓取了2020年1月1日—2020年2月20日期间共计100万条微博数据，   
# 并对其中10万条数据进行人工标注，   
# 标注分为三类，分别为：1（积极），0（中性）和-1（消极）。
# 
# 1. 数据探索 
# 2. 数据分析 
# 3. 数据集构造 
# 4. 解决方案

# In[1]:


get_ipython().system('ls raw_data/')


# ## 1. 数据集探索
# 1. 训练集 
# 2. 测试集 
# 3. 未标记语料 
# 4. 文本清理 

# In[2]:


import pandas as pd

import warnings
warnings.filterwarnings('ignore')


# ### 1.1 训练集

# In[3]:


# 读取训练数据集
raw_train_df = pd.read_csv('raw_data/nCoV_100k_train.labled.csv')
raw_train_df.head()


# In[4]:


# 选取文本相关的列与标签列
subset=['微博中文内容', '情感倾向']

train_df = raw_train_df[subset].dropna(subset=subset).drop_duplicates(['微博中文内容'])
train_df['文本长度'] = train_df['微博中文内容'].apply(lambda x: len(x))
train_df.head()


# In[5]:


# 对每列进行统计分析
for col in train_df.columns:
    print(train_df[col].describe())
    print('=' * 100)


# In[6]:


# 查看标签的唯一值有哪些
train_df['情感倾向'].unique()


# In[7]:


# 查看文本长度等于1的文本内容
train_df[train_df['文本长度'] == 1]


# In[8]:


# 选取正常标签的样本
train_df['good_sample'] = train_df['情感倾向'].apply(lambda x: x in ['-1', '0', '1'])
train_df[train_df['good_sample'].isin(['-1','0','1'])][subset].head()


# In[9]:


# 将中文列名转化为英文
train_df = train_df[train_df['good_sample']][subset]
train_df.rename(columns={'微博中文内容':'text', '情感倾向': 'label', '文本长度': 'text_length'}, inplace=True)
train_df.head()


# ### 1.2 测试集

# In[10]:


raw_test_df = pd.read_csv('raw_data/nCov_10k_test.csv')
raw_test_df.head()


# In[11]:


test_df = raw_test_df[['微博中文内容']].dropna().drop_duplicates()
test_df.rename(columns={'微博中文内容':'text'}, inplace=True)
test_df.describe()


# ### 1.3 未标记语料

# In[12]:


raw_unlabeled_df = pd.read_csv('raw_data/nCoV_900k_train.unlabled.csv')
raw_unlabeled_df.head()


# In[13]:


unlabeled_df = raw_unlabeled_df[['微博中文内容']].dropna().drop_duplicates()
unlabeled_df.rename(columns={'微博中文内容':'text'}, inplace=True)
unlabeled_df.describe()


# ### 1.4 文本清理

# In[14]:


# 随机抽取20条文本，查看文本内容
for text in train_df['text'].sample(20):
    print(text)
    print('=' * 100)


# ### 文本特殊模式总结
# 
# 1.回复、转发@的用户名：   //@快乐源泉李小半， //@李易峰:  
# 2.话题、标签： #抗击新型肺炎第一线#， #记录抗疫时光#  #摄影#          
# 3.表情：   
# 4.微博特有词：展开全文、网页链接、展开全文c  
# 5.网址： 
# 
# 使用正则表达式进行模式匹配，清除无用的文本   
# https://tool.oschina.net/uploads/apidocs/jquery/regexp.html

# In[15]:


import re

# 1. 回复、转发@的用户名
pattern = '(//@)[^: ]+\:'
re.sub(pattern, ' ', '宁波//@京城吃货日记:这人我在罗马见过2-3次，罗马的厨师，宁波人，靠谱，单身。//@捞陈今天惨遭爆破了吗:看这个菜单就知道靠谱//@京城吃货日记:宁波的靠谱意大利餐外卖#最新疫情地图#')


# In[16]:


# 4. 微博特有词：展开全文、网页链接、展开全文c
pattern = '[(转发微博)(\??展开全文c?)(网页链接\??)]'
re.sub(pattern, '', '转发微博 哈哈 网页链接? 每天有180-200万只?展开全文c')


# In[17]:


# 5. 网址
pattern = 'https?:\/\/\w+\.[a-z]{2,6}(\/[\da-zA-Z\_\-]*)*'
re.sub(pattern, '====', '快来加入陕西中医药大学超话和我一起聊聊吧~超话传送门→http://t.cn/RmUGDIM?')


# In[18]:


def clean_text(text):
    pattern = 'https?:\/\/\w+\.[a-z]{2,6}(\/[\da-zA-Z\_\-]*)*'
    text = re.sub(pattern, ' ', text)
    pattern = '[(转发微博)(\??展开全文c?)(网页链接\??)]'
    text = re.sub(pattern, ' ', text)
    pattern = '(//@)[^: ]+\:'
    text = re.sub(pattern, ' ', text)
    pattern = '\s{2,}'  #合并连续的空格
    text = re.sub(pattern, ' ', text)
    text = text.strip().lower() # 去掉两边多余的空格，将大写转小写
    return text


# In[19]:


text = '//@捞陈今天惨遭爆破了吗:看这个菜单就知道靠谱//@京城吃货日记:超话传送门→http://t.cn/RmUGDIM?哈哈哈?展开全文c'
clean_text(text)


# In[20]:


train_df['text'] = train_df['text'].apply(lambda x: clean_text(x))
train_df = train_df[train_df['text'] != '']
train_df.head()


# In[21]:


test_df['text'] = test_df['text'].apply(lambda x: clean_text(x))
test_df = test_df[test_df['text'] != '']
test_df.head()


# In[22]:


unlabeled_df['text'] = unlabeled_df['text'].apply(lambda x: clean_text(x))
unlabeled_df = unlabeled_df[unlabeled_df['text'] != '']
unlabeled_df.head()


# ## 2. 数据分析  
# 1. 查看标签内容
# 2. 文本长度分布    
# 3. 文本标签分布 
# 4. 文本词云构造

# ### 2.1 查看标签内容

# In[23]:


# 对每个标签随机抽取3条文本，查看文本内容
for label, group in train_df.groupby(by='label'):
    print(label)
    print()
    sentences = group.sample(3)['text'].tolist()
    print('\n\n'.join(sentences))
    print("=" * 30)


# ### 2.2 文本长度分布

# In[24]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# In[25]:


train_df['text_length'] = train_df['text'].apply(lambda x: len(x))
train_df.head()


# In[26]:


# 训练集文本长度分布

sns.set()
sns.distplot(train_df['text_length'])
plt.show()


# In[27]:


# 测试集文本分布

test_df['text_length'] = test_df['text'].apply(lambda x: len(x))
sns.set()
sns.distplot(test_df['text_length'])
plt.show()


# #### 文本长度分布结果：
# 1. 文本长度在0-240之间  
# 2. 主要集中在150以内，在140左右分布最多 
# 3. 训练集与测试集保持相同的分布

# ### 2.3 文本标签分布

# In[28]:


# 训练集文本各标签分布情况
plt.figure(figsize=[9,7])
train_df['label'].value_counts().plot.pie(autopct='%1.2f%%')
plt.show()


# In[29]:


# 各标签文本长度分布情况，分为[0, 100], [100-140], [140-240]三档

def text_length_bucket(text_length):
    if text_length < 100:
        return '<100'
    elif 100 <= text_length < 140:
        return '100-140'
    else:
        return '>=140'

train_df['text_length_bucket'] = train_df['text_length'].apply(text_length_bucket)

sns.countplot('label',hue='text_length_bucket',data=train_df)

plt.xlabel('length',fontsize=15)
plt.ylabel('count',fontsize=15)
plt.legend(loc='upper right')
plt.show()


# #### 文本标签分布结果：
# 1. 各标签文本数量分布不均衡，分别为 [17.96, 56.83, 25.21]  
# 2. 各标签文本长度分布一致，大多数集中在<100以内

# ### 2.4 文本词云构造
# 
# “词云”就是通过形成“关键词云层”或“关键词渲染”，对网络文本中出现频率较高的“关键词”的视觉上的突出。词云图过滤掉大量的文本信息，使浏览网页者只要一眼扫过文本就可以领略文本的主旨。

# In[30]:


import jieba

text = '写在年末冬初孩子流感的第五天，我们仍然没有忘记热情拥抱这2020年的第一天。'
words = ' '.join(jieba.lcut(text))
words


# In[31]:


with open('./data/baidu_stopwords.txt', 'r') as f:
    stop_words = f.read().split('\n')

def cut_and_clean(text):
    cuted_text = ' '.join([x for x in jieba.lcut(text) if x not in stop_words and len(x) > 1])
    clean_text = re.sub('([\.，。、“”‘ ’？\?:#：【】\+!！])', ' ', cuted_text)
    clean_text = re.sub('\s{2,}', ' ', clean_text)
    return clean_text

cut_and_clean(text)


# In[32]:


train_text = ' '.join(train_df['text'].apply(cut_and_clean))
train_text[:1000]


# In[33]:


import wordcloud
WC = wordcloud.WordCloud(font_path='./data/MSYH.TTC', 
                         max_words=1000,
                         height= 600,
                         width=1200,
                         background_color='white',
                         repeat=False,
                         mode='RGBA')


# In[34]:


word_cloud_img = WC.generate(train_text)
plt.figure(figsize = (20,10))
plt.imshow(word_cloud_img, interpolation='nearest')
plt.axis("off")
WC.to_file('./data/wordcloud.png')


# ## 3. 数据集构造 
# 1. 划分训练与验证集
# 2. 合并无标签的数据

# In[35]:


print(f"trian data count: {len(train_df)}")
print(f"test data count: {len(test_df)}")
print(f"unlabeled data count: {len(unlabeled_df)}")


# ### 3.1 划分训练与验证集
# ### 90000 -> 80000训练 + 10000验证

# In[36]:


from sklearn.model_selection import train_test_split

# 将标签[-1, 0, 1] 转化为 [0, 1, 2]
train_df['label'] = train_df['label'].apply(lambda x: int(x)+1).astype(int)

# 将有标签的训练数据集划分为训练、测试
train, test = train_test_split(train_df, test_size=10000, random_state=100)

len(train), len(test)


# In[37]:


train[['text', 'label']].to_csv('./processed_data/train.csv', index=False, encoding='utf-8')
test[['text', 'label']].to_csv('./processed_data/test.csv', index=False, encoding='utf-8')


# ### 3.2 合并无标签的数据
# 训练 + 测试 + 未标记

# In[38]:


# 将所有的数据集合并在一起，构造相应的语料集

unlabeled = pd.concat([train_df[['text']], test_df[['text']], unlabeled_df])
unlabeled.head()


# In[39]:


unlabeled.count()


# In[40]:


unlabeled.to_csv('./processed_data/unlabeled.csv', index=False, encoding='utf-8')


# ## 4. 解决方案思考
# ### 240字以内、样本不均衡、“新冠肺炎”相关的文本3分类问题
# ### 
# 在机器学习中，样本不均衡是非常常见的现象。目前来看处理样本不均衡主要有一下三类方法：
# 
# 1. 增加所需要的样本 
# 2. 过采样或者负采样，构造平衡的样本分布 
# 3. 训练中对每个类别添加不同的权重, 损失函数加权 
# 
# #### 接下来的实战中会介绍在Xgboost和Tensorflow中是如何处理样本不均衡的问题。

# In[ ]:





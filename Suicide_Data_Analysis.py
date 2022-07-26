#!/usr/bin/env python
# coding: utf-8

# ## Suicides in India -- Analysis ( Year : 2001 to 2012 )

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


suicide_df = pd.read_csv('Suicides in India 2001-2012.csv')


# In[3]:


suicide_df.head()


# In[4]:


suicide_df.info()


# In[5]:


# As the 'Total' column indicates the number of suicde, total=0 does not make any sense in the dataset.  
suicide_df = suicide_df[suicide_df.Total!=0]


# In[6]:


suicide_df.sample(10)


# In[7]:


suicide_df['Age_group'].unique()


# In[8]:


# I can't understand what is '0-100+' as all other age groups are also in this range.
suicide_df = suicide_df[suicide_df.Age_group != '0-100+']
suicide_df.sample(10)


# In[9]:


suicide_df['Age_group'].unique()


# In[10]:


suicide_df.shape


# In[11]:


starting_year = suicide_df['Year'].min()
ending_year = suicide_df['Year'].max()
print(f'The dataset contains data from {starting_year} to {ending_year}')


# In[12]:


States = pd.DataFrame(suicide_df['State'].unique(),columns =['State'])


# In[13]:


print('Indian states where the data is collected from : \n\n',States)


# ## State - Suicide 

# In[14]:


statewise = suicide_df[['State','Total']].groupby('State').sum().reset_index()


# In[15]:


statewise.sample(10)


# In[16]:


statewise = statewise.sort_values('Total',ascending = False)


# In[17]:


# Visualization
plt.figure(figsize= (20,10)) 
plt.rcParams.update({'font.size':15})
sns.barplot(x ='State', y ='Total', data = statewise)
plt.title('State wise Suicide count')
plt.xticks(rotation = 90)
plt.show()


# In[18]:


# Top 10 States

print('Top 10 States that recorded highest number of suicides : \n\n',statewise.set_index('State').head(10))


# In[19]:


suicide_reason = suicide_df[suicide_df['Type_code'] == 'Causes']
suicide_reason['Type'].value_counts()


# In[20]:


# Category correction 
pd.options.mode.chained_assignment = None
suicide_reason.loc[suicide_reason['Type']=='Bankruptcy or Sudden change in Economic Status', 'Type'] = 'Bankruptcy or Sudden change in Economic Status'
suicide_reason.loc[suicide_reason['Type']=='Bankruptcy or Sudden change in Economic', 'Type'] = 'Bankruptcy or Sudden change in Economic Status'
suicide_reason.loc[suicide_reason['Type']=='Not having Children(Barrenness/Impotency', 'Type'] = 'Not having Children'
suicide_reason.loc[suicide_reason['Type']=='Not having Children (Barrenness/Impotency', 'Type'] = 'Not having Children'
suicide_reason.loc[suicide_reason['Type']=='Causes Not known', 'Type'] = 'Unknown'
suicide_reason.loc[suicide_reason['Type']=='Other Causes (Please Specity)', 'Type'] = 'Unknown'


# In[21]:


suicide_reason['Type'].value_counts()


# ## Suicide Reasons ( Each State )

# In[22]:


states_suicide_df = suicide_reason[['Type','State','Total']]
states = list(states_suicide_df['State'].value_counts().index)
for state in states:
    each_state = states_suicide_df[states_suicide_df['State'] == state ].groupby('Type').sum().sort_values('Total', ascending = False)
    each_state.plot(kind = 'bar', figsize = (20,5), title = state + ' Suicide Reasons',color = 'pink')
    plt.show()


# ## Year - Suicide

# In[23]:


yearwise = suicide_df[['Year','Total']].groupby('Year').sum().reset_index()
yearwise.sample(10)


# In[24]:


yearwise = yearwise.sort_values('Total',ascending = False)


# In[25]:


# Visualization
plt.figure(figsize= (20,10)) 
plt.rcParams.update({'font.size':15})
sns.barplot(x ='Year', y ='Total', data = yearwise)
plt.title('Year wise Suicide count')
plt.show()


# In[26]:


print('Maximum Suicide recorded : \n')
print(yearwise[yearwise['Total']==yearwise['Total'].max()].set_index('Year'))


# In[27]:


print('Minimum Suicide recorded : \n')
print(yearwise[yearwise['Total']==yearwise['Total'].min()].set_index('Year'))


# In[28]:


# rate = {(max -min)/min}*100

rate_of_increment = (yearwise['Total'].max()-yearwise['Total'].min())/yearwise['Total'].min()*100
print('Rate of Increment : {} %'.format(rate_of_increment))
print('Rate of Increment(Rounded) : {} %'.format(round(rate_of_increment)))


# ## Year - Gender - Suicide

# In[29]:


# Visualization
yearwise_gender = suicide_df[['Year','Gender','Total']].groupby(['Year','Gender']).sum()
yearwise_gender = yearwise_gender.reset_index()
plt.figure(figsize= (20,10)) 
plt.rcParams.update({'font.size':15})
sns.barplot(x ='Year', y ='Total',hue='Gender',data = yearwise_gender)
plt.title('Male and Female Suicide count(Yearly)')
plt.show()


# ## Reasons for suicide

# In[30]:


reasonwise = suicide_reason[['Type','Total']].groupby('Type').sum()
reasonwise = reasonwise.sort_values('Total',ascending = False)
reasonwise = reasonwise.reset_index()


# In[31]:


plt.rcParams.update({'font.size': 15})
plt.figure(figsize= (20,15))
sns.barplot(x ='Type', y ='Total', data = reasonwise)
plt.title('Reasons for Suicides vs Number of Suicides')    
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()


# ## Suicide Reasons - Gender

# In[32]:


# suicide Reasons for Male

gender_reason_df = suicide_reason[['Type','Gender','Total']]
male_df = gender_reason_df[gender_reason_df['Gender'] == 'Male']
male_df =  male_df.groupby('Type').sum().reset_index()
male_df_1 = male_df.sort_values('Total', ascending = False)
male_df_1 = male_df_1.reset_index(drop = True)
male_df


# In[33]:


#Visualization

plt.figure(figsize=(20,10))
sns.barplot(x='Type',y='Total',data = male_df_1)
plt.xticks(rotation = 90)
plt.title("Reasons for Suicide (Male)")
plt.show()


# In[34]:


# suicide Reasons for Female

female_df = gender_reason_df[gender_reason_df['Gender'] == 'Female']
female_df = female_df.groupby('Type').sum().reset_index()
female_df_1 = female_df.sort_values('Total', ascending = False)
female_df_1 = female_df_1.reset_index(drop = True)
female_df


# In[35]:


#Visualization

plt.figure(figsize=(20,10))
sns.barplot(x='Type',y='Total',data = female_df_1)
plt.xticks(rotation = 90)
plt.title("Reasons for Suicide (Female)")
plt.show()


# In[36]:


male_female_df = pd.concat([male_df,female_df],axis=1)
male_female_df.columns = ['Type','Male','Type_','Female']
male_female_df.drop('Type_',axis=1,inplace= True)
male_female_df


# ## Male - Female Comparision 

# In[37]:


fig = plt.figure(figsize=(20,8))
N= len(male_female_df)
ind = np.arange(N)
width = 0.4 
category = list(male_female_df['Type'])
plt.bar(x = ind, height = 'Female', data = male_female_df, width = width,label = 'female')
plt.bar(x = ind+width, height = 'Male', data = male_female_df, width = width,label='male')
plt.xlabel("Type of Suicide") 
plt.ylabel("Numeber of Suicides")
plt.title("All Suides Reasons ")
plt.xticks(ind + width / 2, category,rotation='vertical')
plt.legend(loc='best')
plt.show()


# In[38]:


extra_male = male_female_df[male_female_df['Male'] > male_female_df['Female']]
fig = plt.figure(figsize=(20,8))
N= len(extra_male)
ind = np.arange(N)
width = 0.4 
category = list(extra_male['Type'])
plt.bar(x = ind, height = 'Female', data = extra_male, width = width,label = 'female')
plt.bar(x = ind+width, height = 'Male', data = extra_male, width = width,label='male')
plt.xlabel("Type of Suicide") 
plt.ylabel("Numeber of Suicides")
plt.title("All Suides Reasons where Male Suicides are More")
plt.xticks(ind + width / 2, category,rotation='vertical')
plt.legend(loc='best')
plt.show()


# In[39]:


extra_female = male_female_df[male_female_df['Male'] < male_female_df['Female']]
fig = plt.figure(figsize=(20,8))
N= len(extra_female)
ind = np.arange(N)
width = 0.4 
category = list(extra_female['Type'])
plt.bar(x = ind, height = 'Female', data = extra_female, width = width,label = 'female')
plt.bar(x = ind+width, height = 'Male', data = extra_female, width = width,label='male')
plt.xlabel("Type of Suicide") 
plt.ylabel("Numeber of Suicides")
plt.title("All Suides Reasons where Female Suicides are More")
plt.xticks(ind + width / 2, category,rotation='vertical')
plt.legend(loc='best')
plt.show()


# ## Conclusion 
# ## 1. Men seem to be more vulnerable to commit suicide
# ## 2. Unknown reasons are highest, That means Data collection is not effective enough
# ## 3. Family Problems is the known strongest reason

# In[ ]:





# ## Age - Suicide

# In[40]:


agewise = suicide_df[['Age_group','Total']].groupby('Age_group').sum()
agewise


# In[41]:


agewise = agewise.sort_values('Total',ascending = False)
agewise = agewise.reset_index()
agewise


# In[42]:


# Visualization
plt.figure(figsize= (20,10)) 
plt.rcParams.update({'font.size':15})
sns.barplot(x ='Age_group', y ='Total', data = agewise)
plt.title('Age group wise Suicide count')
plt.show()


# ## Age - Suicide Reason

# In[43]:


age_reason_df = suicide_reason[['Type','Age_group','Total']]
age_groups = list(age_reason_df['Age_group'].unique())
for age in age_groups:
    each_group = age_reason_df[age_reason_df['Age_group'] == age ].groupby('Type').sum().sort_values('Total', ascending = False)
    each_group.plot(kind = 'bar', figsize = (20,5), title = 'Age group '+ age + ' Suicide Reasons',color = 'pink')
    plt.show()


# ## Conclusions :
# 
# ## Age group 0-14 : Failure in Examination is the second Strong reason
# ## Age group 0-14, 15-29 : Love affairs is one of the top 5 reasons
# ## Family Problems is the strongest reason in all the age groups
# 
# ## Unknown reasons are highest, That means Data collection is not effective enough

# In[ ]:





# ## How  reasons are changing ?

# In[44]:


year_reasons = suicide_reason[['Year', 'Type', 'Total']]
year_reasons = year_reasons.groupby(['Type', 'Year']).sum().reset_index()
reasons = list(year_reasons['Type'].unique())
for reason in reasons:
    plt.rcParams.update({'font.size': 15})
    plt.figure(figsize = (15,5))
    each_reason = year_reasons[year_reasons['Type'] == reason]
    plt.plot( 'Year', 'Total', data=each_reason, marker='o', markerfacecolor='yellow', markersize=15, color='red', linewidth=3)
    plt.title(reason + '-- from 2001 to 2012')
    plt.show()


# ## How suicide rate is changing ?

# In[45]:


yearwise = yearwise.sort_values('Year',ascending = True)
yearwise


# In[46]:


Death_per_year = list(yearwise['Total'])


# In[47]:


suicide_rate_year = [round(((Death_per_year[i]-Death_per_year[i-1])/Death_per_year[i-1])*100,2) for i in range(1,len(Death_per_year))]


# In[48]:


suicide_rate_year


# In[49]:


for i in range(1,len(suicide_rate_year)):
    suicide_rate_year[i]=round(suicide_rate_year[i-1]+suicide_rate_year[i],2)
suicide_rate_year


# In[50]:


year = list(yearwise['Year'])[1:]
year


# In[51]:


rate_year = pd.DataFrame({
    'Year':year,
    'Suicide_rate':suicide_rate_year
})
rate_year


# In[52]:


plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (15,5))
plt.plot('Year','Suicide_rate',data=rate_year,marker='o',markerfacecolor='red',markersize=15,color='pink',linewidth=3)
plt.title('Suicide rate changing from 2002 to 2012')
plt.show()


# 

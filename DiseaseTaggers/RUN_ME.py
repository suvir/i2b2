
# coding: utf-8

# In[23]:

import os
from feature_builder import build_featurelist
import csv


# In[68]:

def features(token):
    featurelist=[]
    featurelist.append(token.lower())
    featurelist += build_featurelist(token)
    return featurelist


# In[2]:

DATA_DIR = '/Users/suvir/Documents/GWAS/i2b2/Data/raw_data for track 2/risk_bio_new'
MODEL_DIR = '/Users/suvir/Documents/GWAS/i2b2/Data/final_data/feature_files/models'


# In[5]:

data_files = os.listdir(DATA_DIR)
model_files = os.listdir(MODEL_DIR)
data_files = [d for d in data_files if d.endswith('bio')]
model_files = [m for m in model_files if m.endswith('model')]


# In[19]:

get_ipython().system(u'mkdir TEMP')


# 1. Generate feature files for all input files
# 2. Call crf_test on each feature file
# 3. Parse the output of each crf_test model
# 4. Reconstruct original file with labels now
# 5. Clean up any remaining directories

# In[69]:

def generate_features(DATA_DIR,data_file):
    l=open(DATA_DIR+'/'+data_file).readlines()
    #print len(l)
    output_data_file = 'features_'+data_file
    output = open('TEMP/'+output_data_file,'w')
    wr = csv.writer(output, delimiter='\t', quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)
    filename=l[0] #Ignoring first line. It is file name.
    for line in l[1:]:
        if line.startswith('\n'):
            dummy_token='AZUREUS'
            wr.writerow(features(dummy_token))
        else:
            token = line.split('\t')[0]
            wr.writerow(features(token))
    output.close()
    return filename,'TEMP/'+output_data_file
    
for data_file in data_files:
    #These are the files which have the final output of the experiment
    result_file = 'TEMP/'+'RESULT_'+data_file
    final_result = open(result_file,'w')
    
    #Generating features for file
    fn,feature_file = generate_features(DATA_DIR,data_file)
    
    #Because the input file also has first line as filename
    final_result.write(fn) 
    
    #Output_dict has the output of all the CRF models
    output_dict={}
    
    #Generating the CRF output for each trained CRF model
    for model_file in model_files:
        model_name = model_file.split('_')[0]
        full_path_of_model = MODEL_DIR+'/'+model_file
        temp_output = 'TEMP/'+'TEMP_'+model_name
        get_ipython().system(u'crf_test -m $full_path_of_model $feature_file > $temp_output')
        output_dict[model_name]=open(temp_output,'r').readlines()
        #print len(output_dict[model_name]),model_name
    
    #This is the expected number of lines in the file
    file_length = len(output_dict['a1c'])
    
    #Process label for each token as per the CRF models
    for i in range(file_length):
        label_list = []
        flag_label = False
        token = output_dict['a1c'][i].split('\t')[0].strip()
        #print token
        if token == 'AZUREUS':
            #print "NEW LINE"
            final_result.write('\n')
        else:
            for k in output_dict:
                this_label=output_dict[k][i].split('\t')[-1].strip()
                label_list.append(this_label)
            
            for label in label_list:
                if label.startswith('B') or label.startswith('I'):
                    final_result.write(token+'\t'+this_label+'\n')
                    flag_label = True
                    break
            if not flag_label:
                final_result.write(token+'\t'+'O'+'\n')   
    print "Finished processing",data_file


# In[58]:

#!rm TEMP/*


# In[70]:

#!cat TEMP/RESULT_100-05.bio


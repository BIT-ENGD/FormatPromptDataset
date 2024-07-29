import os
import sys 
import json 
import glob
import random 
import math
from shutil import copyfile
DIRLIST=["7ZIP-LZMA","APK","CSS","CSV","BMP","DLL","DOC","DOCX","DWG","ELF","EPS","EPUB","exe","PNG-c0","GIF","GZIP","HTML","ICS","JAVASCRIPT","JPG","POWERSHELL","PPT","PPTX","JSON","lossless-c0","MKV","MP4","ODS","OXPS","MP3","SVG","TAR","RAR","TIF","TXT","XLS","PDF","XLSX","XML","ZIP-LZMA","ZLIB"]
TYPELIST=["7ZIP","APK","CSS","CSV","BMP","DLL","DOC","DOCX","DWG","ELF","EPS","EPUB","exe","PNG","GIF","GZIP","HTML","ICS","JAVASCRIPT","JPG","POWERSHELL","PPT","PPTX","JSON","WEBP","MKV","MP4","ODS","OXPS","MP3","SVG","TAR","RAR","TIF","TXT","XLS","PDF","XLSX","XML","ZIP","ZLIB"]

SRC_DIR="G:\\NapierOne-total"
TARGET_DIR="f:\\all_dataset"
SUFFIX="-total"

def SampleDataset(name,TARGET_DIR,TARGET_TRAIN_NUM=200,TARGET_TEST_NUM=50):

    TARGET_DIR=os.path.join(TARGET_DIR,name)
    if os.path.exists(TARGET_DIR):
        print("The target directory has been existed!")
        exit(-1)
    if not  os.path.exists(TARGET_DIR):
        os.mkdir(TARGET_DIR)




    if not  os.path.exists(TARGET_DIR):
        os.mkdir(TARGET_DIR)

    def enum_dir(src,target_train,target_test,TARGET_TRAIN_NUM,TARGET_TEST_NUM):
        if not os.path.exists(target_train):
            os.mkdir(target_train)
        ext_name = '*.*'
        os.chdir( src )
        FILELIST=[]
        for file in glob.glob( ext_name ):
            info=os.path.splitext(file)
            if(not info[0][0].isnumeric()):
                continue
            FILELIST.append(file)
        if(len(FILELIST) == 0):
            print("no file in the directory:",src)
        if (TARGET_TRAIN_NUM+TARGET_TEST_NUM) > len(FILELIST):
            TARGET_TRAIN_NUM=math.floor(len(FILELIST)*0.8)
            TARGET_TEST_NUM=len(FILELIST) -TARGET_TRAIN_NUM

        train=random.sample(FILELIST,TARGET_TRAIN_NUM)
        FILELIST=list(set(FILELIST).difference(set(train)))
        test=random.sample(FILELIST,TARGET_TEST_NUM)
        for filename in train:
            src_file=os.path.join(src,filename)
            target_file =os.path.join(target_train,filename)
            copyfile(src_file,target_file)

        for filename in test:
            src_file=os.path.join(src,filename)
            target_file =os.path.join(target_test,filename)
            copyfile(src_file,target_file)
        return TARGET_TRAIN_NUM,TARGET_TEST_NUM
        

    TRAIN_DIR=os.path.join(TARGET_DIR,"train")
    TEST_DIR=os.path.join(TARGET_DIR,"test")
    if(not os.path.exists(TRAIN_DIR)):
        os.mkdir(TRAIN_DIR)
        os.mkdir(TEST_DIR)

    ACTUAL_NUM=dict()
    for id,dir in enumerate(DIRLIST):
        typedir=os.path.join(SRC_DIR,(dir+SUFFIX))
        if not os.path.exists(typedir):
            print("directory is not existed:",typedir)
        target_train_dir=os.path.join(TRAIN_DIR,dir)
        target_test_dir=os.path.join(TEST_DIR,dir)
        if(not os.path.exists(target_train_dir)):
            os.mkdir(target_train_dir)
            os.mkdir(target_test_dir)


        if not os.path.exists(typedir):
            print("bad directory:",typedir)
        train_num, test_num=enum_dir(typedir,target_train_dir,target_test_dir,TARGET_TRAIN_NUM,TARGET_TEST_NUM)
        ACTUAL_NUM[id]=[train_num,test_num]
        
        

    CLASSINF=dict()
    for id,item in zip(range(0,len(TYPELIST)),TYPELIST):
        CLASSINF[id]=[item,DIRLIST[id],ACTUAL_NUM[id]]

    with open(os.path.join(TARGET_DIR,"classinfo.json"),"w") as f:
        json.dump(CLASSINF,f)
        


if __name__ == "__main__":
    #SampleDataset("sample_500",TARGET_DIR,400, 100)
    #SampleDataset("sample_1000",TARGET_DIR,800, 200)
    #SampleDataset("sample_2500",TARGET_DIR,1600, 400)
    SampleDataset("sample_2500",TARGET_DIR,2000, 500)
    SampleDataset("sample_5000",TARGET_DIR,4000, 1000)

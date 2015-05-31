__author__ = 'SRIZVI'
#31-05-2015
#This program takes Movies directory or the movie file as input.
#It makes entries in the MySQL DB for the movie files or movie files in the directories
#If whole source is passed as input Dir, Program will refresh the complete table i.e. delete and insert again.

import os
import sys
import re
import urllib
import json

def nameCorrection(text, wordDic):
    rc = re.compile('|'.join(map(re.escape, wordDic)))
    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)


#This method will return the movie file names after recursively walking to whole dir
def returnFullFileNames(path):
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if
              os.path.splitext(f)[1] in FILE_TYPES]
    return result

#This func will fetch the language of movie as they are saved and will make inserts for DB
def get_imdb_rating(basename,year):
    imdb_rating = "0"
    lang = ""
    try:
        if str(year) != '0':
            url = "http://www.omdbapi.com/?t=" + basename+"&y="+str(year)
        else:
            url = "http://www.omdbapi.com/?t=" + basename
        print url
        response = urllib.urlopen(url).read()
        jsonvalues = json.loads(response)
        if jsonvalues["Response"] == "True":
            imdb_rating =  jsonvalues['imdbRating']
            lang = jsonvalues['Language']
            return imdb_rating,lang
        else:
            return imdb_rating,lang
    except IOError:
        return imdb_rating,lang




def handleFiles(path,mode):
    result = []
    if mode == 0:
        result = returnFullFileNames(path)
    else:
        root, extension = os.path.splitext(path)
        if extension in FILE_TYPES:
            result = [path]

    for file_name in result:
        f = open(INSERT_SQL, 'a')
        if re.search('HINDI', os.path.dirname(file_name)):
            lang = LANG_HIN
        else:
            lang = LANG_ENG

        file_name = file_name.replace("'s", "")
        basename= os.path.splitext(os.path.basename(file_name).upper())[0]
        if not re.search('sample', file_name, re.IGNORECASE):
            basename = nameCorrection(basename,wordDic)
            basename=basename.replace("."," ")
            basename=basename.rstrip()
            basename=basename.lstrip()
            p = re.search(r'[12]\d{3}',basename)
            if p is not None:
                basename=basename[0:p.end()+1]
                imdb_rating,imdb_lang=get_imdb_rating(basename[0:p.start()], basename[p.start():p.end()])
            else:
                imdb_rating,imdb_lang=get_imdb_rating(basename,0)
            if not imdb_lang == "":
                lang = imdb_lang
            file_name=file_name.replace("\\","\\\\")
            try:
                f.write(INSERT_QUE_PREFIX +basename+ SINGLE_QUOTE + ",'"+lang+"',"+ SINGLE_QUOTE + imdb_rating +SINGLE_QUOTE+ "," + SINGLE_QUOTE +os.path.splitdrive(os.path.dirname(file_name))[1]+"');" + "\n")
                f.close()
            except TypeError:
                pass
            except IOError:
                pass


    os.system(INSERT_BATCH)

def main():
    if len(sys.argv) == 1:
        print "This program needs at least one dir in parameter"
        sys.exit(1)
    try:
        os.remove(INSERT_SQL)
    except OSError:
        pass
    for path in sys.argv:
        if os.path.isdir(path) and os.path.splitdrive(path)[1] == COMPLETE_SOURCE:   #Full DB Refresh, Whole Sources is passed as input Dir
            os.system(DELETE_BACTH)
            handleFiles(path,0)
        elif os.path.isdir(path):
            handleFiles(path,0)
        else:
            handleFiles(path,1)


def var_initialization():
    global COMPLETE_SOURCE, INSERT_SQL, INSERT_BATCH, DELETE_BACTH, INSERT_QUE_PREFIX, LANG_HIN, LANG_ENG, SINGLE_QUOTE, FILE_TYPES
    COMPLETE_SOURCE = "\\DATA\\Movies"
    INSERT_SQL = 'C:\\Users\\srizvi.NTNET\\PycharmProjects\\\MovieDatabase\\movie_insert.sql'
    INSERT_BATCH = 'C:\\Users\\srizvi.NTNET\\PycharmProjects\\\MovieDatabase\\movie_insert.bat'
    DELETE_BACTH = 'C:\\Users\\srizvi.NTNET\\PycharmProjects\\\MovieDatabase\\movie_delete.bat'
    INSERT_QUE_PREFIX = "INSERT IGNORE INTO MOVIE (name,language,imdb_rating,location) VALUES('"
    LANG_HIN = "Hindi"
    LANG_ENG = "English"
    SINGLE_QUOTE = "'"
    FILE_TYPES = ['.mkv', '.avi', '.mp4', '.mkv', '.mpg', '.mpeg', '.rm', '.vob', '.wmv', '.flv', '.3gp', '.DAT',
                  '.divx']


if __name__  == '__main__':
    wordDic = {'IMBT':'','DVD':'','[':' ', ']':' ','{':' ','}':' ','-':' ','_':' ','@':'','CD1':'','CD2':'','CD3':'','Dual-Audio':'','DUAL AUDIO':'','CD4':'',')':' ','(':' ','1080P':'','720P':'','BRRIP':'','XVID':'','AC3':'','BDRIP':'','DVDRIP':'','X264':'','BLURAY':'','YIFY':'','BRRIPX264':'','BLU-RAY':'','DVDSCR':'','EXCLUSIVE':'','RIP':'','DDR':'','CDRIP':'' ,'DIVX':'','FLAWL3SS':''}
    var_initialization()
    main()

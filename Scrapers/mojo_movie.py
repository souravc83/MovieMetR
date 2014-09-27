#global imports
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import json
import time
import pandas as pd
from collections import OrderedDict
import os
import pickle

#local imports
from mojo_weekly_chart import WeeklyChart


class MojoMovie(object):
    """
    this scrapes information from each movie
    from a given list of movies from the website
    www.boxofficemojo.com
    """

    def __init__(self,moviejson):
        self._baseurl='http://www.boxofficemojo.com'
        self._jsonfile=moviejson
        self._dictlist_picklefile='dictlist.pickle'
        #to be defined later
        self._ordered_movie_dict=None;

        self._list_of_dicts=None
        

    def _read_jsonfile(self):
        json_data=open(self._jsonfile)
        self._ordered_movie_dict=json.load(json_data,object_pairs_hook=\
                                           OrderedDict)
        json_data.close()

    def getmoviedetails(self):
        self._read_jsonfile()
        self._load_saved_dictlist()
        
        
        counter=0;
        startval=len(self._list_of_dicts)
        endval=len(self._ordered_movie_dict)
        
        for item in self._ordered_movie_dict.items():
            print counter
            if counter<startval:
                counter+=1
                continue
            if counter>800:
                break
            try:
                
                (movielink,moviename)=item
                print "Trying: ",movielink             
                self._process_movie(movielink)
                print "Processed: ",movielink," : ",moviename
            except:
                break
            counter+=1
            
        pickle.dump(self._list_of_dicts,file(self._dictlist_picklefile,'w'))
        return

    def _load_saved_dictlist(self):
        if os.path.isfile(self._dictlist_picklefile) ==True:
            self._list_of_dicts=pickle.load(file(self._dictlist_picklefile))
        else:
            self._list_of_dicts=[]
        return
        

    def _process_movie(self,movielink):
        movie_url=self._baseurl+movielink;
        try:
            html_page=urlopen(movie_url)
        except:
            print 'Could not open: '+movie_url
            raise ValueError
        #if try succeeds
        soup_page=BeautifulSoup(html_page,"lxml")

        moviedict={}
        moviedict["moviename"]=(self._ordered_movie_dict[movielink]).encode('utf-8')
        moviedict["movie_url"]=movielink.encode('utf-8')

        #put everything in try,except blocks to handle
        #null values if a field isn't available
        
        try:
            self._table_at_top(moviedict,soup_page)
        except:
            pass

        mp_boxes=soup_page.find_all("div",{"class":"mp_box"})
        
        if len(mp_boxes)!=0:
            for box in mp_boxes:
                box_tab=box.find("div",{"class":"mp_box_tab"})
                box_txt=box_tab.get_text().encode('utf-8')
            
                if box_txt == "Total Lifetime Grosses":
                    try:
                        self._lifetime_gross(moviedict,box)
                    except:
                        pass
            
            if box_txt=='The Players':
                try:
                    self._find_actors(moviedict,box)
                except:
                    pass
            
            if box_txt=="Domestic Summary":
                try:
                    self._domestic_summary(moviedict,box)
                except:
                    pass
            if box_txt=="Genres":
                try:
                    self._get_genres(moviedict,box)
                except:
                    pass
        
        #weekly chart
        try:
            self._get_weekly_chart(moviedict,movie_url)
        except:
            pass
        
        #after adding all values to this moviedict
        self._list_of_dicts.append(moviedict)
        return

        
    
    def _lifetime_gross(self,newdict,box):
        content_table=box.find("div",{"class":"mp_box_content"}).find("table")
        all_data=content_table.find_all("td")
        data_text=[]
        for data in all_data:
            data_text.append(data.get_text().encode('utf-8'))
        
        for i in range(len(data_text)):
            if data_text[i]=='Domestic:':
                newdict["domestic_gross"]=self._extract_digits(data_text[i+1])
            if re.search("Foreign:$",data_text[i]) is not None:
                newdict["foreign_gross"]=self._extract_digits(data_text[i+1])
            if re.search("Worldwide:$",data_text[i]) is not None:
                newdict["worldwide_gross"]=self._extract_digits(data_text[i+1])
                
        return
    
    def _extract_digits(self,raw_str):
        #new_str=raw_str.encode('utf-8')
        pattern='(\d.+)'
        m=re.search(pattern,raw_str)
        result=m.group(0)
        result=re.sub(',','',result)
        return result
    
    def _find_actors(self,newdict,box):
        content_table=box.find("div",{"class":"mp_box_content"}).find("table")
        all_data=content_table.find_all("td")
        data_text=[]
        for data in all_data:
            data_text.append(data.get_text().encode('utf-8'))
        
        for i in range(len(data_text)):
            if data_text[i]=="Director:":
                newdict["director"]=data_text[i+1]
            if data_text[i]=='Writer:':
                newdict["writer"]=data_text[i+1]
                
            if data_text[i]=='Actors:':
                #print data_text[i+1] #if we use this version,
                #we need to seperate first names, last names
                #otherwise list only major actors
                
                actor_list=all_data[i+1].find_all("a")
                actor_list=[actor.get_text().encode('utf-8') for actor in actor_list]
                newdict["actors"]=actor_list
        return
                

    def _domestic_summary(self,newdict,box):
        content_tables=box.find("div",{"class":"mp_box_content"}).find_all("table")
        all_data=[]
        for table in content_tables:
            for some_data in table.find_all("td"):
                all_data.append(some_data)
        data_text=[]
        for data in all_data:
            data_text.append(data.get_text().encode('utf-8'))
        
        for i in range(len(data_text)):
            #print data_text[i]
            if re.search('(Weekend:$)',data_text[i]) is not None:
                newdict["opening_weekend"]=self._extract_digits(data_text[i+1])
            
            if re.search("(^Widest)",data_text[i]) is not None:
                theaters=re.sub('\xc2\xa0','',data_text[i+1])
                theaters=re.sub(' theaters','',theaters)
                newdict["widest_release_theaters"]=theaters #str2num?
            
            if re.search("^Close",data_text[i]) is not None:
                newdict["close_date"]=re.sub('\xc2\xa0','',data_text[i+1])
            
            if re.search("In\sRelease",data_text[i]) is not None:
                m=re.search('(\d+)',data_text[i+1])
                newdict["days_running"]=m.group(1)
          

    def _get_genres(self,newdict,box):
        content_table=box.find("div",{"class":"mp_box_content"}).find("table")
        all_hyperlinks=content_table.find_all("a")
        genre_list=[]
        
        for link in all_hyperlinks:
            genre_list.append(link.get_text().encode('utf-8'))
        
        newdict['genre']=genre_list
        return
        

    def _get_weekly_chart(self,newdict,movie_url):
        
        movie_specific=re.sub('http://www.boxofficemojo.com/movies/\?','',movie_url)
        
        weekly_url='http://www.boxofficemojo.com/movies/?page=weekly&'+movie_specific
        chart=WeeklyChart(newdict,weekly_url)
        chart.scrapechart()
        return
    
    def _table_at_top(self,newdict,soup_page):
        top_table=soup_page.find("table",{"width":"95%"})
        
        all_cols=top_table.find_all("td")
        
        for i in range(len(all_cols)):
            distributor=all_cols[1].get_text().encode('utf-8')
            newdict["distributor"]=re.sub("Distributor: ",'',distributor)
            release_date=all_cols[2].get_text().encode('utf-8')
            newdict["release_date"]=re.sub("Release Date: ",'',release_date)
            genre_toplist=all_cols[3].get_text().encode('utf-8')
            newdict["genre_toplist"]=re.sub("Genre: ",'',genre_toplist)
            runtime=all_cols[4].get_text().encode('utf-8')
            newdict["runtime"]=re.sub("Runtime: ",'',runtime)
            mpaa_rating=all_cols[5].get_text().encode('utf-8')
            newdict["mpaa_rating"]=re.sub("MPAA Rating: ",'',mpaa_rating)
            prod_budget=all_cols[6].get_text().encode('utf-8')
            newdict["production_budget"]=re.sub("Production Budget: ",'',prod_budget)
        
        return
        
    

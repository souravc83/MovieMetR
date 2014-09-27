"""
checks whether a zipcode is 
valid and returns a location
corresponding to the zipcode
"""

#global imports
import sqlite3

#local imports



class CheckZip(object):

    def __init__(self,zipcode):
        self._zipcode=zipcode #should this be int(zipcode)
        self._iserror=False
        self._database_name='us_zipcodes.db'
        #to be defined later
        self._con=None
        self._cursor=None

    def _basiccheck(self):
        """
        checks whether zip is 5 digit number
        """
        zipstr=str(self._zipcode)
        if len(zipstr)==5:
            self._iserror=False
        else:
            self._iserror=True
        return

    def _query_db(self):
        """
        queries database to find location
        """  
        self._con=sqlite3.connect(self._database_name)
        self._cursor=self._con.cursor()
        query='SELECT city,state\
               FROM uszipcodes\
               WHERE zipcode=%d'%self._zipcode;
        self._cursor.execute(query)
                              
        loc_data=self._cursor.fetchall()

        if len(loc_data)==0:
            self._iserror=True
            return None
        else:
            city,state=loc_data
            placestr=city+", "+state
            return placestr
       

    def get_location(self):
        self._basiccheck()
        location=self._query_db()

        if location is not None:
            locstr=location+" "+str(self._zipcode)
        else
            locstr="Pittsburgh, PA"+" " +str(15232)

        return locstr,self._iserror
                
        
   

class check:
    '''
    This is a module to...
    check null value , ...
    fill null value and ...
    standardize to any data 
    '''
    
    def __init__(self,df):
        self.df = df
        
    def isnull(self,df):
        '''
        This function will check the ...
        
        null value present in your dataframe
        '''
        return self.df.isnull().sum()
    
    def fillna(self,df):
        '''
        This function will fill the ...
        null value as per your requirement...
        
        This function stores mean , median and mode...
        of a data frame having null values. ...
        
        Then it asks user to what they want to fill in place of null value ...
        wheather floating number as per there wish ...
        or mean median or mode...
        
        After getting input from user it stores ...
        floating number given by user or mean or median...
        or mode...
        
        If user select mode then this module ...
        will store the minimum value of the mode. ...
        '''
        try:
            p = self.df.columns.tolist()
            
            for i in range(len(p)):
                
                if self.df.dtypes[p[i]] == 'int64' or 'float64':
                    
                    if self.df[p[i]].isnull().sum() > 0:
                        
                        print(p[i],"has null value")
                        
                        j = input("what you want to replace float or mean or median or mode(give one choice out of 4):")

                        mean = self.df[p[i]].mean()
                        median = self.df[p[i]].median()
                        mode = self.df[p[i]].mode()

                        if j == "float":   
                            l = float(input("Enter number as per your choice:"))
                            self.df[p[i]].fillna(value = l, inplace=True)
                        
                        elif j == "mean":
                            self.df[p[i]].fillna(value = mean, inplace=True)
                        
                        elif j == "median":
                            self.df[p[i]].fillna(value = median, inplace=True)
                        
                        elif j == "mode":
                            self.df[p[i]].fillna(value = min(mode), inplace=True)
                else:
                    if self.df[p[i]].isnull().sum() > 0:
                        
                        print(p[i],"has null value")
                        
                        j = input("Please enter:")
                        
                        self.df[p[i]].fillna(value=j, inplace=True)
        
        except Exception as e:
            
            print("Error occured",e)
            
    def standard(self,feature):
        '''
        this function will standardize ... 
        any array or feature column ...
        as per your wish ...
        '''
        from sklearn.preprocessing import StandardScaler 
        scaler = StandardScaler ()
        arr = scaler.fit_transform(feature)
        return arr
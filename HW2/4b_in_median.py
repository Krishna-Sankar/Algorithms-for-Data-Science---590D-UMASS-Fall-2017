from mrjob.job import MRJob
from mrjob.job import MRStep

class HashtagCount(MRJob):

    def map(self, _, tweet):
        """
        Output the number of hashtags and a count for each tweet
        the '_' can be used when there is no key
        """
        #num_hashtags = sum(1  for i in tweet.split() if i.startswith("#"))
        temp_list=tweet.strip().split('\t')
        #yield int(temp_list[0]), int(temp_list[1])
        yield int(temp_list[1]),int(temp_list[0])

    def reduce_source_len(self,key,value):
        length=0
        for i in value:
            length+=1
        yield key,length

    def reduce_const_len(self,key,value):
        #print type(value)
        int_val=int(next(value))
        #print "int_val",int_val
        yield 1,int_val
    
    def reduce1(self, key, value):
        # a simple sum function
        out_deg=[]
        for i in value:
            out_deg.append(i)
        #print "OUT",out_deg
        yield 1,out_deg

    def reduce_sort(self,key,value):
        out_deg1=[]
        out_deg1=next(value)
        #for i in value:
        #    out_deg1.append(i)
        out_deg1.sort()
        #print "OUT",out_deg1
        yield 1,out_deg1

    def reduce_median_count(self,key,value):
        print"I am here"
        c=0
        out_deg1=[]
        out_deg1=next(value)
        count=len(out_deg1)
        '''count=sum(1 for x in next(value))'''
        #for i in value:
        #    c+=1
        #count=c
        print "Hi"
        v=[1,2,3]
        yield count,out_deg1

    def reduce_median(self,key,value):
        out=[]
        out=next(value)
        #print "length of out",len(out)
        print "OUT",out
        print "key",key
        if (key%2!=0):
            med=out[(key+1)/2-1]
        else:
            med=((out[(key/2)-1] + out[((key)/2)])/2.0)
        yield "Median",med




    def steps(self):
        """
        the steps can be modified to compose any number of map/reduce steps
        by including multiple instances of self.mr
        """
        return[
            MRStep(mapper=self.map,
                   reducer=self.reduce_source_len),
            MRStep(reducer=self.reduce_const_len),
            MRStep(reducer=self.reduce1),
            MRStep(reducer=self.reduce_sort),
            MRStep(reducer=self.reduce_median_count),
            MRStep(reducer=self.reduce_median)
              ]


if __name__ == '__main__':
    HashtagCount.run()

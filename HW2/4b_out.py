from mrjob.job import MRJob
from mrjob.job import MRStep

class HashtagCount(MRJob):

    def map(self, _, tweet):
        """
        Map each source node to the corresponding destination
        """
        #num_hashtags = sum(1  for i in tweet.split() if i.startswith("#"))
        temp_list=tweet.strip().split('\t')
        yield int(temp_list[0]), int(temp_list[1])
        #yield int(temp_list[1]),int(temp_list[0])

    def reduce_source_len(self,key,value):
        '''
        use the reducer to map each key to the length of the values in the list 
        '''
        length=0
        for i in value:
            length+=1
        yield key,length

    def reduce_const_len(self,key,value):
        '''
        use the reducer to map all the lengths to a constant key 
        '''
        #print type(value)
        int_val=int(next(value))
        #print "int_val",int_val
        yield 1,int_val

 

    #def combiner_const_to_key(self,key,value):
       # yield 1,key

    def reduce(self, key, value):
        '''
        Count the number of values in the combine list to get the total outdegree 
        '''
        # a simple sum function
        totalV=0
        for i in value:
          totalV+=i
          #print"total",totalV
          #print"i",i
        #print"total",totalV

        yield "Outdegree",totalV

    def reduce_avg(self, key, value):
        #calculating average
        avg=int(next(value))/265214.0
        yield "average",avg


    def steps(self):
        """
        the steps can be modified to compose any number of map/reduce steps
        by including multiple instances of self.mr
        """
        return[
            MRStep(mapper=self.map,
                   reducer=self.reduce_source_len),
            MRStep(reducer=self.reduce_const_len),
            MRStep(reducer=self.reduce),
            MRStep(reducer=self.reduce_avg)
              ]


if __name__ == '__main__':
    HashtagCount.run()

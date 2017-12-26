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

    def reduce_greater_than(self,key,value):
        length=next(value)
        print(length)
        count=0
        if (length>2):
            
            count+=1   
        print "count =",count
        val=[1,2,3]
        yield 1,count

    def reduce_sum_greater(self,key,value):
        yield 1,sum(value)

    def steps(self):
        """
        the steps can be modified to compose any number of map/reduce steps
        by including multiple instances of self.mr
        """
        return[
            MRStep(mapper=self.map,
                   reducer=self.reduce_source_len),
            MRStep(reducer=self.reduce_greater_than),
            MRStep(reducer=self.reduce_sum_greater)
              ]


if __name__ == '__main__':
    HashtagCount.run()

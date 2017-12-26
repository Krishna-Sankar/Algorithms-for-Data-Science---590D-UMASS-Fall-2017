from mrjob.job import MRJob
from mrjob.job import MRStep

class HashtagCount(MRJob):

    def map(self, _, tweet):
        """
       Map each source node to the corresponding destination and each destiination to the corresponding source. 
        """
        #num_hashtags = sum(1  for i in tweet.split() if i.startswith("#"))
        temp_list=tweet.strip().split('\t')
        #global totalV
        #totalV=0
        yield int(temp_list[0]), int(temp_list[1])
        yield int(temp_list[1]),int(temp_list[0])

    def combiner_const_to_key(self,key,value):
        """
        Use the combiner to map all the nodes to a single key
        """
        yield 1,key

    def reduce(self, key, value):
        """
        Counting the number of nodes in value will give us the total number of nodes in the graph
        """
        totalV=0
        for i in value:
          totalV+=1
        yield "Total number of nodes",totalV


    def steps(self):
        """
        the steps can be modified to compose any number of map/reduce steps
        by including multiple instances of self.mr
        """
        #return [MRStep(mapper=self.map,
                       # combiner=self.reduce,
                        #reducer=self.reduce)]

        return [MRStep(mapper=self.map,
                        reducer=self.combiner_const_to_key),
            MRStep(reducer=self.reduce)]



if __name__ == '__main__':
    HashtagCount.run()

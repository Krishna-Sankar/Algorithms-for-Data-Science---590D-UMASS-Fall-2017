from mrjob.job import MRJob
from mrjob.job import MRStep


class HashtagCount(MRJob):
   # def __init__

    def map_init(self):
        global pass_list
        pass_list = []
        global num_nodes
        num_nodes = 265214

    def map_source(self, _, tweet):
        """
        Output the number of hashtags and a count for each tweet
        the '_' can be used when there is no key
        """
        # num_hashtags = sum(1  for i in tweet.split() if i.startswith("#"))
        temp_list = tweet.strip().split('\t')
        # print("map1")
        yield 1, int(temp_list[1])
        yield 2, int(temp_list[0])

    def map_final(self):
        pass

    def red(self, key, value):
        s = []
        d = []
        # pass_list=[]
        if(key == 1):
            for i in value:
                s.append(i)
            pass_list.append(s)

        else:
            for j in value:
                d.append(j)
            pass_list.append(d)

        #print ("pass list", pass_list)
        # print"s= ",len(s)
        # print "d= ",len(d)
        set_s = set()
        for k in s:
            set_s.add(k)
        set_d = set()
        for l in d:
            set_d.add(l)
        # print(set_d)
        # print(set_s)
        # print("answer!!",set_s.intersection(set_d))
        #print("answer!!",set_s & (set_d))
        yield 1, pass_list

    def red2(self, key, value):
        temp_list1 = []
        temp_list2 = []
        count = 0
        for i in value:

            if (len(i) == 2):
                # print(len(i))
                #print("i = ", i, "count = ", count)
                temp_list1.append(i[0])
                temp_list2.append(i[1])
            count += 1

        #print ("one:", temp_list1)
        #print ("two", temp_list2)
        ans = ()
        s = ()
        d = ()
        # for k in temp_list1
        s = set(temp_list1[0])
        d = set(temp_list2[0])
        ans = s & d
        l1 = list(ans)
        u1 = []
        u2 = []
        u1 = temp_list1[0]
        u2 = temp_list2[0]
        # temp_list1.append(temp_list2)
        # print "temp", temp_list1#$,temp_list1[1]
        hops = []
        # print l1
        for i in l1:

            #p = max(u1.count(i), u2.count(i))
            p = (u1.count(i) * u2.count(i))

            # print "Number: ",i,"Hops:",p
            hops.append(p)
        # print "hops", hops

        #print("Answer!", ans)
        yield 1, hops

    def red3(self, key, value):
        temp = []
        for i in value:
            temp.append(i)
        s = sum(temp[0])
        avg = s / num_nodes
        p = "Sum is " + str(s) + "  Average is  " + str(avg) +" "
        temp[0].sort()
        # print temp[0]
        l = []
        l = temp[0]
        a = len(temp[0])
        if (a % 2 != 0):
            med = l[(a + 1) / 2 - 1]
        else:
            med = ((l[(a / 2) - 1] + l[((a) / 2)]) / 2)
        p = p + "Median is " + str(med)
        yield "", p

    def steps(self):
        """
        the steps can be modified to compose any number of map/reduce steps
        by including multiple instances of self.mr
        """
        return[
            MRStep(mapper_init=self.map_init, mapper=self.map_source, mapper_final=self.map_final, reducer=self.red),
            MRStep(reducer=self.red2), MRStep(reducer=self.red3)

        ]


if __name__ == '__main__':
    HashtagCount.run()

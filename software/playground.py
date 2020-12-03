#try class attributes and method

    #TODO: fill this out
        # the above dict has
        #key =  
            #(no_of_switches, primary_direction)
        #value
            #dict containing:
            #key = 
                # first switch # encountered when circling clockwise indexed from 0
            #value = 
                #conversion matrix


class test:
    classatr = dict()

    def add_to_dict(key, val):
        if key not in test.classatr.keys():
            test.classatr[key] = val

    def print_stuff():
        print(test.classatr)

    def __init__(self, key, val):
        test.add_to_dict(key, val)
    
    def inst_print_stuff(self):
        test.print_stuff()


t1 = test(0,"zero")
test.classatr[1] = "one"

test.add_to_dict(3, "three")

t2 = test(0,"three")
test.print_stuff()

t2.inst_print_stuff()
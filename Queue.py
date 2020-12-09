import numpy as np
import random
import matplotlib.pyplot as plt
import tqdm
from Passenger import Passenger

class Queue:
    '''
    This is the base class representation of a queue to board a 3x3 configuration airplane.
    Initialize with the number of seat rows on the plane.
    If visual_mode argument is True, an ASCII representation of the current seat status is printed after every step for visualization purposes.
    Recommended for visual_mode to be False during automated simulation, very messy otherwise.
    '''
    
    def __init__(self, rows, visual_mode = False):
        self.rows = rows
        self.queue = self.generate_queue()
        self.visual_mode = visual_mode

        self.seats = np.full(shape = (rows+1,7), fill_value = '__', dtype = 'object')
        self.seats[:,3] = '||'
        self.seats[rows] = np.array(['AA','BB','CC','  ','DD','EE','FF'])


    # Returns a list of of passengers.
    # If pasn_only argument is True, no buffer tiles (||) are included at the start of the queue; for debug only.
    
    def generate_queue(self, pasn_only = False):
        pasn_num = 6*self.rows
        queue = []
        for pasn in range(pasn_num):
            queue.append(Passenger(pasn//6, pasn%6))

        if not pasn_only:
            queue =  self._add_buffer(queue)

        return queue

    def _add_buffer(self, queue):
        return self.rows * ['||'] + queue

    # Processes the actions of every passenger for one time step.
    # Returns True if all passengers are seated.
    def step(self):
        # Step through all queue 'tiles'
        for idx, pasn in enumerate(self.queue):
            if pasn == '||':
                pass

            # If tile contains a passenger who's at his row
            elif self.rows - 1 - pasn.row == idx:
                if pasn.storing == False:
                    pasn.storing = True

                elif pasn.storing:
                    if pasn.slow and not pasn.storing_slow:
                        pasn.storing_slow = True
                    elif not pasn.slow or pasn.storing_slow:
                        pasn.storing = False
                        pasn.storing_slow = False
                        self.queue[idx] = '||'

            elif self.queue[idx-1] == '||':
                self.queue[idx-1] = pasn
                self.queue[idx] = '||'
                
        if self.visual_mode:
            pre_queue = self.queue[self.rows:self.rows + 4]
            self.seats[:-1,3] = self.queue[:self.rows]
            print(pre_queue)
            print(self.seats)

        if self.queue.count('||') == self.rows*7:
            return True

        else:
            return False

    # Function to simulate one round of boarding.
    # Returns the number of time steps elapsed.
    def simulate(self):
        count = 0
        while not self.step():
            count += 1

        return count


class RandomQueue(Queue):
    '''
    Subclass of Queue class representing a random queue order.
    '''
    
    name = 'Random'
    
    def generate_queue(self, pasn_only = False):
        pasn_num = 6*self.rows
        queue = []
        for pasn in range(pasn_num):
            queue.append(Passenger(pasn//6, pasn%6))
            
        random.shuffle(queue)
        if not pasn_only:
            queue = self._add_buffer(queue)
                
        return queue


class B2FQueue(Queue):
    '''
    Subclass representing a back-to-front queue ordering.
    '''
    
    name = 'B2F'

    def generate_queue(self, pasn_only = False):
        pasn_num = 6*self.rows
        queue = []
        for pasn in range(pasn_num):
            queue.append(Passenger(pasn//6, pasn%6))
            
        back = queue[:pasn_num//3]
        middle = queue[pasn_num//3:pasn_num//3*2]
        front = queue[pasn_num//3*2:]

        random.shuffle(back)
        random.shuffle(middle)
        random.shuffle(front)

        queue[:pasn_num//3] = back
        queue[pasn_num//3:pasn_num//3*2] = middle
        queue[pasn_num//3*2:] = front

        if not pasn_only:
            queue = self._add_buffer(queue)
                
        return queue


class F2BQueue(Queue):
    '''
    Subclass representing a front-to-back queue ordering.
    '''
    
    name = 'F2B'

    def generate_queue(self, pasn_only = False):
        pasn_num = 6*self.rows
        queue = []
        for pasn in range(pasn_num):
            queue.append(Passenger(pasn//6, pasn%6))
            
        back = queue[:pasn_num//3]
        middle = queue[pasn_num//3:pasn_num//3*2]
        front = queue[pasn_num//3*2:]

        random.shuffle(back)
        random.shuffle(middle)
        random.shuffle(front)

        queue[:pasn_num//3] = back
        queue[pasn_num//3:pasn_num//3*2] = middle
        queue[pasn_num//3*2:] = front

        queue.reverse()
        
        if not pasn_only:
            queue = self._add_buffer(queue)
                
        return queue


class WMAQueue(Queue):
    '''
    Subclass representing a window-middle-aisle queue ordering.
    '''
    
    name = 'WMA'

    def generate_queue(self, pasn_only = False):
        queue = []
        for section in [[0,5],[1,4],[2,3]]:
            sub_queue = []
            for side in section:
                for row in range(self.rows):
                    sub_queue.append(Passenger(row,side))
            random.shuffle(sub_queue)
            queue += sub_queue

        if not pasn_only:
            queue = self._add_buffer(queue)
                
        return queue


class SteffenQueue(Queue):
    '''
    Subclass representing a queue ordering using the Steffen method.
    '''
    
    name = 'Steffen'

    def generate_queue(self, pasn_only = False):
        queue = []
        for letter in [0,5,1,4,2,3]:
            for row in range(self.rows-1, -1, -1):
                queue.append(Passenger(row, letter))

        if not pasn_only:
            queue = self._add_buffer(queue)
                
        return queue     


class SteffenModifiedQueue(Queue):
    '''
    Subclass representing a queue ordering using a modified Steffen method (AKA Pyramid method).
    '''
    
    name = 'Steffen mod.'

    def generate_queue(self, pasn_only = False):
        queue = []
        for row in np.flip(np.array(range(self.rows))[0::3]):
            for letter in [0,1,2]:
                queue.append(Passenger(row, letter))
        for row in np.flip(np.array(range(self.rows))[0::3]):
            for letter in [5,4,3]:
                queue.append(Passenger(row, letter))
        for row in np.flip(np.array(range(self.rows))[1::3]):
            for letter in [0,1,2]:
                queue.append(Passenger(row, letter))
        for row in np.flip(np.array(range(self.rows))[1::3]):
            for letter in [5,4,3]:
                queue.append(Passenger(row, letter))
        for row in np.flip(np.array(range(self.rows))[2::3]):
            for letter in [0,1,2]:
                queue.append(Passenger(row, letter))
        for row in np.flip(np.array(range(self.rows))[2::3]):
            for letter in [5,4,3]:
                queue.append(Passenger(row, letter))

        if not pasn_only:
            queue = self._add_buffer(queue)
                
        return queue 


def complete_simul(rows, iterations = 100):
    data = {}
    
    print('Random boarding')
    random_data = []
    for i in tqdm.tqdm(range(iterations)):
        sim = RandomQueue(rows)
        random_data.append(sim.simulate())
    data[sim.name] = random_data        

    print('f2b boarding')
    f2b_data = []
    for i in tqdm.tqdm(range(iterations)):
        sim = F2BQueue(rows)
        f2b_data.append(sim.simulate())
    data[sim.name] = f2b_data  

    print('b2f boarding')
    b2f_data = []
    for i in tqdm.tqdm(range(iterations)):
        sim = B2FQueue(rows)
        b2f_data.append(sim.simulate())
    data[sim.name] = b2f_data  

    print('wma boarding')
    wma_data = []
    for i in tqdm.tqdm(range(iterations)):
        sim = WMAQueue(rows)
        wma_data.append(sim.simulate())
    data[sim.name] = wma_data  

    print('Steffen boarding')
    steffen_data = []
    for i in tqdm.tqdm(range(iterations)):
        sim = SteffenQueue(rows)
        steffen_data.append(sim.simulate())
    data[sim.name] = steffen_data  

    print('Steffen modified boarding')
    steffen_m_data = []
    for i in tqdm.tqdm(range(iterations)):
        sim = SteffenModifiedQueue(rows)
        steffen_m_data.append(sim.simulate())
    data[sim.name] = steffen_m_data
    
    for item in data:
        plt.hist(data[item], label = item, histtype = 'stepfilled', alpha = 0.5)
        plt.axvline(avg(data[item]), linewidth = 2, dashes = (2,1))
        plt.text(avg(data[item]), 46, str(avg(data[item])), horizontalalignment='center', verticalalignment='center', color = 'blue', fontsize = 12)

    plt.title('Timing Distributions from Boarding Simulations (i = {})'.format(iterations), pad = 45)
    plt.xlabel('No. ticks to completion')
    plt.ylim((0,45))

    plt.legend()
    plt.show()

def avg(data):
    return sum(data)/len(data)


if __name__ == '__main__':
    a = complete_simul(9, 100)

# Airplane Boarding Simulation Framework

## About
This project attempts to be an exetensible module for simulating various methods for airplane boarding.

## Usage
The `Queue` class along with its subclasses are used to perform a simulation and return it's elapsed timing. Each subclass represents one boarding method. The following is a simple example to perform one simulation using the `RandomQueue` subclass:

```python
from Queue import RandomQueue

queue = RandomQueue(rows = 9)
elapsed = queue.simulate()
```

There are currently 6 methods implemented:

### RandomQueue
Passengers are ordered in random fashion.

### B2FQueue
Back-to-Front order. Seats are divided into 3 groups, the back, middle and front; passengers in the back are sent in first, those in the front last. Intra-group order is random.

### F2BQueue
Front-to-Back order. Same as B2F except front is first and back is last.

### WMAQueue
Window-middle-aisle ordering. Passengers seated closest to the window are sent in first, followed by those in the middle and then aisle seats.

### SteffenQueue
Ordering based on the Steffen Method.

### SteffenModifiedQueue
Ordering based on the 'Pyramid' Method.

### Custom Queues
Custom queue orderings can easily be included by subclassing the base `Queue` class. Please follow the following template when subclassing your own method:

```python
class CustomQueue(Queue):
    name = 'Custom name'
    
    def generate_queue(self, pasn_only = False):
        # Create your queue here.
        
        if not pasn_only:
            queue = self._add_buffer(queue)
        return queue
```

The `generate_queue` method must return a list of `Passenger` objects. Each `Passenger` object can accept a `row` (0 to row size) and `seat` (0-5) argument. The `self.rows` attribute contains the number of airplane rows. The `Passenger` class can also be edited in Passenger.py to alter its attributes.

The `complete_simul` function is included to quickly simulate and plot all 6 methods using pyplot:

```python
complete_simul(rows = 9, iterations = 100)
```
![alt text](https://github.com/DarrelYee/Airplane-Boarding-Simulation-Framework/blob/main/Figure_6.png?raw=true)

## References
Video from CGP Grey that inspired this project:
https://www.youtube.com/watch?v=oAHbLRjF0vo

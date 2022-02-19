```go
type LoopQueue struct {
	Entries []interface{}
	Head    uint16
	Tail    uint16
	Length  uint16

	lock sync.Mutex
}

func NewLoopQueue(length uint16) (*LoopQueue, error) {
	lq := &LoopQueue{
		Entries: make([]interface{}, length+1),
		Length:  length + 1,
		Head:    0,
		Tail:    0,
	}

	return lq, nil
}

func (lq *LoopQueue) Enqueue(v interface{}) error {
	defer lq.lock.Unlock()
	lq.lock.Lock()

	if ((lq.Tail + 1) % lq.Length) == lq.Head {
		return fmt.Errorf("queue is full")
	}

	lq.Entries[lq.Tail] = v
	lq.Tail = (lq.Tail + 1) % lq.Length

	return nil
}

func (lq *LoopQueue) Dequeue() (interface{}, error) {
	defer lq.lock.Unlock()
	lq.lock.Lock()

	if lq.Head == lq.Tail {
		return nil, fmt.Errorf("queue is empty")
	}

	entry := lq.Entries[lq.Head]
	lq.Head = (lq.Head + 1) % lq.Length

	return entry, nil
}
```
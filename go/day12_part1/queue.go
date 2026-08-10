package main

type Queue[T any] struct {
	elements []T
}

func (q *Queue[T]) append(p T) {
	q.elements = append(q.elements, p)
}

func (q *Queue[T]) popleft() T {
	point := q.elements[0]
	q.elements = q.elements[1:]
	return point
}

func (q *Queue[T]) pop() T {
	point := q.elements[len(q.elements)-1]
	q.elements = q.elements[:len(q.elements)-1]
	return point
}

func (q *Queue[T]) is_empty() bool {
	return len(q.elements) == 0
}

func (q *Queue[T]) len() int {
	return len(q.elements)
}

func NewQueue[T any]() *Queue[T] {
	return &Queue[T]{[]T{}}
}

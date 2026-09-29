package main

// Visited Set
type Set[T comparable] struct {
	elements map[T]bool
}

func (s *Set[T]) add(p T) {
	s.elements[p] = true
}

func (s *Set[T]) remove(p T) {
	delete(s.elements, p)
}

func (s *Set[T]) contains(p T) bool {
	_, ok := s.elements[p]
	return ok
}

func (s *Set[T]) is_empty() bool {
	return len(s.elements) == 0
}

func (s *Set[T]) len() int {
	return len(s.elements)
}

func (s *Set[T]) list_of_elements() []T {
	keys := []T{}
	for point := range s.elements {
		keys = append(keys, point)
	}
	return keys
}

func (s *Set[T]) copy() *Set[T] {
	new_visited := NewSet[T]()
	for key, value := range s.elements {
		new_visited.elements[key] = value
	}
	return new_visited
}

func (s *Set[T]) union(s2 *Set[T]) *Set[T] {
	union_set := s.copy()
	for key, value := range s2.elements {
		union_set.elements[key] = value
	}
	return union_set
}

func (s *Set[T]) difference(s2 *Set[T]) *Set[T] {
	diff := s.copy()
	for key := range s2.elements {
		diff.remove(key)
	}
	return diff
}

func (s *Set[T]) intersection(s2 *Set[T]) *Set[T] {
	inter_set := NewSet[T]()
	for key := range s2.elements {
		if s.contains(key) {
			inter_set.add(key)
		}
	}
	return inter_set
}

func NewSet[T comparable]() *Set[T] {
	return &Set[T]{make(map[T]bool)}
}

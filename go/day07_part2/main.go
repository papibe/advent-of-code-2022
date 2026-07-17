package main

import (
	"fmt"
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Command int

const (
	CD = iota
	LS
	FILE
	DIR
	ERROR
)

type Dir struct {
	name   string
	size   int
	dirs   map[string]*Dir
	files  map[string]*File
	parent *Dir
}

type File struct {
	name   string
	size   int
	parent *Dir
}

func NewDir(name string, parent *Dir) *Dir {
	dir := Dir{
		name,
		0,
		make(map[string]*Dir),
		make(map[string]*File),
		parent,
	}
	return &dir
}

func (d *Dir) add_file(file *File) {
	d.files[file.name] = file
}

func (d *Dir) add_dir(dir *Dir) {
	d.dirs[dir.name] = dir
}

func (d *Dir) update_dir_sizes() {

	var dfs func(d *Dir) int
	dfs = func(d *Dir) int {
		if d == nil {
			return 0
		}
		current_size := 0

		for _, file := range d.files {
			current_size += file.size
		}
		for _, dir := range d.dirs {
			current_size += dfs(dir)
		}
		d.size = current_size
		return current_size
	}

	_ = dfs(d)
}

func get_token(line string) (Command, string) {
	re_cd_dir := regexp.MustCompile(`\$ cd (\w+)`)
	match := re_cd_dir.FindStringSubmatch(line)
	if len(match) > 0 {
		return CD, match[1]
	}

	re_cd_up := regexp.MustCompile(`\$ cd ..`)
	match = re_cd_up.FindStringSubmatch(line)
	if len(match) > 0 {
		return CD, ".."
	}

	re_cd_root := regexp.MustCompile(`\$ cd /`)
	match = re_cd_root.FindStringSubmatch(line)
	if len(match) > 0 {
		return CD, "/"
	}

	re_dir := regexp.MustCompile(`dir (\w+)`)
	match = re_dir.FindStringSubmatch(line)
	if len(match) > 0 {
		return DIR, match[1]
	}

	re_file := regexp.MustCompile(`(\d+) (.*)$`)
	match = re_file.FindStringSubmatch(line)
	if len(match) > 0 {
		return FILE, match[0]
	}

	re_ls := regexp.MustCompile(`ls`)
	match = re_ls.FindStringSubmatch(line)
	if len(match) > 0 {
		return LS, ""
	}

	return ERROR, ""
}

func parse(filename string) []string {
	data, err := os.ReadFile(filename)
	if err != nil {
		panic("File error")
	}
	return strings.Split(strings.Trim(string(data), "\n"), "\n")
}

func create_filesystem_tree(terminal_output []string) *Dir {
	file_system := NewDir("file_system", nil)
	root := NewDir("/", file_system)
	file_system.add_dir(root)
	current := file_system

	for _, line := range terminal_output {
		command, params := get_token(line)

		switch command {

		case CD:
			if params == ".." {
				current = current.parent
			} else {
				current = current.dirs[params]
			}

		case FILE:
			split_params := strings.Split(params, " ")
			size_str, name := split_params[0], split_params[1]
			size, _ := strconv.Atoi(size_str)
			current.add_file(&File{name, size, current})

		case DIR:
			dir := NewDir(params, current)
			current.add_dir(dir)

		case LS:
			continue

		default:
			panic("unknown token")
		}
	}
	return root
}

func solve(dir *Dir, space_left, space_needed int) int {
	min_size := math.MaxInt

	var dfs func(*Dir, int, int)

	dfs = func(dir *Dir, space_left, space_needed int) {
		if dir == nil {
			return
		}
		if dir.size+space_left >= space_needed {
			min_size = min(min_size, dir.size)
		}
		for _, sub_dir := range dir.dirs {
			dfs(sub_dir, space_left, space_needed)
		}
	}
	dfs(dir, space_left, space_needed)

	return min_size
}

func solution(filename string) int {
	terminal_output := parse(filename)
	root := create_filesystem_tree(terminal_output)
	root.update_dir_sizes()

	space_left := 70_000_000 - root.size

	return solve(root, space_left, 30_000_000)
}

func main() {
	fmt.Println(solution("./example.txt")) // 24933642
	fmt.Println(solution("./input.txt"))   // 5883165
}

#!/usr/bin/python
'''
the cubes
1/1/15
'''
import sys

def print_cube(cube_string, n):
    '''
    prints out the cube floor by floor
    '''
    for floor_pos in xrange(0, len(cube_string), n**2):
        print floor_pos / n**2
        for row_pos in xrange(0, n**2, n):
            string_pos = floor_pos + row_pos
            print cube_string[string_pos: string_pos + n]
        

def build_cube(cube_string, n):
    '''
    reads in string of asterisks, spaces, and 'o'
    converts it into a cube [floor][row][col]
    '''
    cube = []
    for floor_pos in xrange(0, len(cube_string), n**2):
        cube.append([])
        floor_number = floor_pos / (n**2)
        for row_pos in xrange(0, n**2, n):
            string_pos = floor_pos + row_pos
            cube[floor_number].append(list(cube_string[string_pos: string_pos + n]))
    return cube    
    
def get_hole_in_wall(cube, n, floor_number):
    '''
    gets the [row, col] of entrances/exits
    '''
    for pos in xrange(n):
        if cube[floor_number][0][pos] == ' ':
            return (floor_number,0,pos)
        if cube[floor_number][n-1][pos] == ' ':
            return (floor_number,n-1, pos)
        if cube[floor_number][pos][0] == ' ':
            return (floor_number,pos, 0)
        if cube[floor_number][pos][n-1] == ' ':
            return (floor_number,pos, n-1)
    sys.exit('Entrance not found')
    
def solve_cube(cube, n):
    '''
    solve cube by starting at entrance on first floor to
    exit on top floor
    '''
    visited_cube = [[[0 for _ in xrange(n)] for _ in xrange(n)] for _ in xrange(n)]
    entrance_cell = get_hole_in_wall(cube, n, 0)
    exit_cell = get_hole_in_wall(cube, n, n-1)
    positions = set()
    positions.add(entrance_cell)
    floor, row, col = entrance_cell
    visited_cube[floor][row][col] = 1
    number_steps = 0
    while True:
        new_positions = set()
        for position in positions:
            #print position
            floor, row, col = position
            if row > 0 and cube[floor][row-1][col] != '*' and visited_cube[floor][row-1][col] == 0:
                new_positions.add((floor, row-1, col))
                visited_cube[floor][row-1][col] = 1
            if row < n-1 and cube[floor][row+1][col] != '*' and visited_cube[floor][row+1][col] == 0:
                new_positions.add((floor, row+1, col))
                visited_cube[floor][row+1][col] = 1
            if col > 0 and cube[floor][row][col-1] != '*' and visited_cube[floor][row][col-1] == 0:
                new_positions.add((floor, row, col-1))
                visited_cube[floor][row][col-1] = 1
            if col < n-1 and cube[floor][row][col+1] != '*' and visited_cube[floor][row][col+1] == 0:
                new_positions.add((floor, row, col+1))
                visited_cube[floor][row][col+1] = 1
            if floor > 0 and cube[floor][row][col] == 'o' and visited_cube[floor-1][row][col] == 0:
                new_positions.add((floor-1, row, col))
                visited_cube[floor-1][row][col] = 1
            if floor < n-1 and cube[floor+1][row][col] == 'o' and visited_cube[floor+1][row][col] == 0:
                new_positions.add((floor+1, row, col))
                visited_cube[floor+1][row][col] = 1
        number_steps += 1
        if exit_cell in new_positions:
            number_steps += 1
            break
        if len(new_positions) == 0:
            number_steps = 0
            break
        positions = set(new_positions)
        
    print number_steps
                 
with open(sys.argv[1]) as FH:
    for line in FH:
        line = line.rstrip()
        n, cube_string = line.split(';')
        n = int(n)
        cube = build_cube(cube_string, n)
        #print_cube(cube_string, n)
        solve_cube(cube, n)

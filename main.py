from maze_solver import MazeSolver
import argparse

def main(maze_file_path, display):
    maze_solver = MazeSolver(maze_file_path)
    maze_solver.a_star_search(display=display)

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Solve a maze.")

    # Add arguments
    parser.add_argument('-d', '--display', action='store_true',
                        help='Display the state of the maze after each robot move.')
    parser.add_argument('maze_file_path', type=str, 
                        help='Path to the maze definition file.')

    # Parse arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args.maze_file_path, args.display)
    

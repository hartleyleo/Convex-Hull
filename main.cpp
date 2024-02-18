#include <iostream>
#include <string>
#include <cmath>
#include <vector>
#include <utility>

#include "maze.h"

int main(int argc, char** argv) {

    // Check if the correct number of command-line arguments is provided
    if (argc != 5) {
        std::cerr << "Usage: " << argv[0] << " <seed> <rows> <cols> <outputFileName>" << std::endl;
        return 1;
    }

    // Get command-line arguments
    const char* inputFileName = argv[0];
    int seed = std::stoi(argv[1]);
    int rows = std::stoi(argv[2]);
    int cols = std::stoi(argv[3]);
    std::string outputFileName = argv[4]; // Use std::string for file names

    std::vector<std::vector<int> > board(rows, std::vector<int>(cols, 15));

    maze Maze(seed, rows, cols, board, outputFileName);


    return 0;
}

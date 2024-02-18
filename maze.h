#ifndef MAZE_H
#define MAZE_H

#include <iostream>
#include <vector>

class maze {

    private:

        int seed;
        
        int rows;

        int cols;

    public:

        maze();

        maze(int seed, int rows, int cols, std::vector<std::vector<int> >& board, const std::string& filename);

        ~maze();

        void printMaze(int rows, int cols, std::vector<std::vector<int> >& board);

        void printMazeToFile(std::vector<std::vector<int> >& board, const std::string& filename, int rows, int cols);

};

#endif

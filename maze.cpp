#include "maze.h"
#include <cmath>
#include <vector>
#include <iostream>
#include <utility>
#include <fstream>
#include <algorithm>

maze::maze(int inputSeed, int inputRows, int inputCols, std::vector<std::vector<int> >& board, const std::string& filename){
    seed = inputSeed;
    rows = inputRows;
    cols = inputCols;

    int x = 0, y = 0;

    std::srand(seed);

    std::vector<std::pair<int, int> > neighbors;

    std::vector<std::pair<int, int> > visited;

    // create empty dynamic array `A`
    std::vector<std::pair<int, int> > A;
    // mark cell [0,0] as visited
    visited.push_back(std::make_pair(y, x));
    // insert cell [0,0] at the end of `A`
    A.push_back(std::make_pair(y, x));
    // while `A` is not empty
    while (!A.empty()){
    //     `current` <- remove last element from `A`
        // std::pair<int, int> current = A.back();
        A.pop_back();
    //     `neighbors` <- `current`'s neighbors not visited yet
        neighbors.clear();


        std::vector<std::pair<int, int> > test;

        // North
        if (y > 0) {
            bool isVisited = false;

            for (int i = 0; i < visited.size(); i++) {
                if (visited[i].first == y - 1 && visited[i].second == x) {
                // The cell [y, x] has already been visited
                    isVisited = true;
                    test.push_back(std::make_pair(-1, -1));
                    break; // Exit the loop since we found a match
                }
            }

            if (!isVisited) {
                neighbors.push_back(std::make_pair(y - 1, x));
                test.push_back(std::make_pair(y - 1, x));
            }
        }
        // South
        if (y < rows - 1) {
            bool isVisited = false;

            for (int i = 0; i < visited.size(); i++) {
                if (visited[i].first == y + 1 && visited[i].second == x) {
                // The cell [y, x] has already been visited
                    isVisited = true;
                    test.push_back(std::make_pair(-1, -1));
                    break; // Exit the loop since we found a match
                }
            }

            if (!isVisited) {
                neighbors.push_back(std::make_pair(y + 1, x));
                test.push_back(std::make_pair(y + 1, x));
            }
        }
        // East
        if (x < cols - 1) {
            bool isVisited = false;

            for (int i = 0; i < visited.size(); i++) {
                if (visited[i].first == y && visited[i].second == x + 1) {
                // The cell [y, x] has already been visited
                    isVisited = true;
                    test.push_back(std::make_pair(-1, -1));
                    break; // Exit the loop since we found a match
                }
            }

            if (!isVisited) {
                neighbors.push_back(std::make_pair(y, x + 1));
                test.push_back(std::make_pair(y, x + 1));
            }
        }
        // West
        if (x > 0) {
            bool isVisited = false;

            for (int i = 0; i < visited.size(); i++) {
                if (visited[i].first == y && visited[i].second == x - 1) {
                // The cell [y, x] has already been visited
                    isVisited = true;
                    test.push_back(std::make_pair(-1, -1));
                    break; // Exit the loop since we found a match
                }
            }

            if (!isVisited) {
                neighbors.push_back(std::make_pair(y, x - 1));
                test.push_back(std::make_pair(y, x - 1));
            }
        }

        if(neighbors.size() == 0) {
            y = visited[visited.size() - 1].first;
            x = visited[visited.size() - 1].second;
            //board[visited[visited.size() -1].first][visited[visited.size() -1].second] = 15;
            visited.pop_back();
            continue;
        }
        // std::cout << "works";
    //     if `neighbors` is not empty
        if (!neighbors.empty()){
            // std::cout << "works";
    //         insert `current` at the end of `A`
    //         `neigh` <- pick a random neighbor from `neighbors`
                int idx = std::rand() / ((RAND_MAX + 1u) / neighbors.size());
                std::pair<int, int> randomNeighbor = neighbors[idx];
                //neighbors[idx];
                //std::cout << "works";

                int index = 0;

                for (int i = 0; i < test.size() - 1; i++){
                    if (randomNeighbor.first == test[i].first && randomNeighbor.second == test[i].second){
                        index = i;
                        break;
                    }
                }

    //         remove the wall between `current` and `neigh`
                if (x == 0 && y == 0){
                    board[y][x] -= 8;
                    //std::cout << "works";
                    y = randomNeighbor.first;
                    x = randomNeighbor.second;
                } 
                if (x == cols - 1 && y == rows - 1) {
                    board[y][x] -= 4;
                    //std::cout << "works";
                    y = randomNeighbor.first;
                    x = randomNeighbor.second;
                } else {
                    y = randomNeighbor.first;
                    x = randomNeighbor.second;

                    // North
                    if (index == 0) {
                        board[y][x] -= 8;
                        // if (y > 0) {
                        //     board[y + 1][x] -= 4;
                        // }
                    }
                    // South
                    else if (index == 1) {
                   
                        board[y][x] -= 4;
                        // if (y < rows - 1) {
                        //     board[y - 1][x] -= 8;
                        // }
                    }
                    // East
                    else if (index == 2) {
                     
                        board[y][x] -= 2;
                        // if (x < cols - 1) {
                        //     board[y][x + 1] -= 1;
                        // }
                    }
                    // West
                    else if (index == 3) {
    
                        board[y][x] -= 1;
                        // if (x > 0) {
                        //     board[y][x - 1] -= 2;
                        // }

                    } 
                }
                test.clear();
    //         mark `neigh` as visited
                visited.push_back(std::make_pair(y, x));
    //         insert `neigh` at the end of `A`
                A.push_back(std::make_pair(y, x));
    //     endif
        }
    // endwhile
    }

    printMaze(rows, cols, board);

    printMazeToFile(board, filename, rows, cols);
    
}

maze::~maze(){
}

void maze::printMaze(int rows, int cols, std::vector<std::vector<int> >& board){
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            std::cout << board[i][j] << " ";
        }
        std::cout << std::endl;
    }
}


void maze::printMazeToFile(std::vector<std::vector<int> >& board, const std::string& filename, int rows, int cols) {
    // Open the file for writing
    std::ofstream outputFile(filename);

    // Check if the file is successfully opened
    if (!outputFile.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }

    // Write maze data to the file
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            outputFile << board[i][j] << " ";
        }
        outputFile << std::endl;
    }

    // Close the file
    outputFile.close();

    std::cout << "Maze successfully printed to file: " << filename << std::endl;
}
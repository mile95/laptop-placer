# Laptop Placer

Command line tool for automagic placement of your macOS laptop on the given side of your external monitor.

Heavily inspired by and dependent on [displayplacer](https://github.com/jakehilborn/displayplacer).

Laptop Placer automates placing your laptop to the `right`, `left` or `below` your single external monitor.
A special use case of [displayplacer](https://github.com/jakehilborn/displayplacer).


## Requirements

You guessed it, [displayplacer](https://github.com/jakehilborn/displayplacer).

    brew tap jakehilborn/jakehilborn && brew install displayplacer

## Installation

    git clone git@github.com:mile95/laptop-placer.git

## Usage

    cd laptop-placer
    python3 laptop_placer.py --pos left
![image](https://user-images.githubusercontent.com/8545435/198119890-88a4d866-7275-4125-b8e4-2fc3f5cdee7e.png)

    cd laptop-placer
    python3 laptop_placer.py --pos right

![image](https://user-images.githubusercontent.com/8545435/198120166-656b67d0-a919-4824-9f77-9b485c2b88b5.png)

    cd laptop-placer
    python3 laptop_placer.py --pos below

![image](https://user-images.githubusercontent.com/8545435/198120329-3a215189-35a0-45d3-9441-6b531934901b.png)

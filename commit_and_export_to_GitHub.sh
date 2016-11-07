#! /bin/bash

cd '/home/vlad/Programs/My_projects/games/OASIS/code-upbge'
hg status
hg commit
hg bookmark -r default master
hg push OASIS

#!/bin/bash
cd out
for ((i = 563;i>0;i--)); do
    tar -xvf $i.tar
    rm $i.tar
done

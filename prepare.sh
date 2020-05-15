#!/bin/sh

if [ "x$1" = "xtravis" ]; then
    alias antlr4='java -cp "../../antlr.jar:$CLASSPATH" org.antlr.v4.Tool'
fi

cd $(dirname "$0")/formlang/query && antlr4 -Dlanguage=Python3 -visitor query.g4

#!/bin/sh

cd $(dirname "$0")/formlang/query && antlr4 -Dlanguage=Python3 -visitor query.g4

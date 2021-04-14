#!/bin/bash

# Make sure we can reach our libraries via lib/ even if they were originally put into lib64/

if [ -d "$INSTALL_DIR/install/lib64" ]; then

    if ! [ -d "$INSTALL_DIR/install/lib" ]; then
        ln -s ${INSTALL_DIR}/install/lib64 ${INSTALL_DIR}/install/lib
    fi
fi

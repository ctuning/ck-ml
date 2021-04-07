#!/bin/bash

function exit_if_error() {
    if [ "${?}" != "0" ]; then exit 1; fi
}

fix_input_shape=${_FIX_INPUT_SHAPE:-NO}
echo "Fix input shape? ${fix_input_shape}"
echo

if [ "${fix_input_shape}" != "NO" ]; then
  read -d '' CMD <<EO_CMD
"${CK_ENV_COMPILER_PYTHON_FILE}" "${ORIGINAL_PACKAGE_DIR}/fix_input_shape.py" \
--input_name   "${MODEL_INPUT_LAYER_NAME}"   \
--input_graph  "${PACKAGE_NAME}"             \
--output_graph "${PACKAGE_NAME}"             \
--type b
EO_CMD
  echo ${CMD}
  eval ${CMD}
  echo
fi
exit_if_error

echo "Done."
exit 0

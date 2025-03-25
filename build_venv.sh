export BASE_DIR=/opt/hpc4ag
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$BASE_DIR/uv" sh
source $BASE_DIR/uv/env
export UV_PYTHON_INSTALL_DIR=$BASE_DIR/uv/python_installs/
uv python install 3.12
uv venv --python=3.12 $BASE_DIR/venv
source $BASE_DIR/venv/bin/activate
uv pip install --link-mode=copy -r requirements.txt
uv pip install --link-mode=copy ./
chmod -R g+rx $BASE_DIR/uv
chmod -R g+rx $BASE_DIR/venv

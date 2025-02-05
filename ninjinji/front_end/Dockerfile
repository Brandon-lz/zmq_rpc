# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# 先执行
# reflex export
# unzip backend.zip -d backend
# 修改文件front_end/rxconfig.py中的dbhost为docker环境的host（因为打包需要，暂时先设置了localhost）
# docker build --no-cache . -t backend


# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1


# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=~/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
# ADD . /app
COPY backend ./
RUN --mount=type=cache,target=~/.cache/uv \
    uv sync --frozen --no-dev 

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONUNBUFFERED=1

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

EXPOSE 8000

# Run the FastAPI application by default
# Uses `fastapi dev` to enable hot-reloading when the `watch` sync occurs
# Uses `--host 0.0.0.0` to allow access from outside the container
CMD ["reflex", "run", "--backend-only","--env","prod"]

# API_URL=http://localhost:8000 reflex export
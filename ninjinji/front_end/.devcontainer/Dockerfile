FROM mcr.microsoft.com/devcontainers/python:1-3.10-bullseye

ENV PYTHONUNBUFFERED 1

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>


RUN sudo ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# RUN pip install --upgrade pip --proxy="http://10.30.24.88:7890" && pip install -r requirements.txt --proxy="http://10.30.24.88:7890"

# export https_proxy=http://10.30.24.88:7890
# export http_proxy=http://10.30.24.88:7890

# https_proxy=http://10.30.24.88:7890 http_proxy=http://10.30.24.88:7890 reflex export --frontend-only --no-zip
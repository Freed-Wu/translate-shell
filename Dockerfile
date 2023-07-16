#!/usr/bin/env -S docker build -tfreedwu/translate-shell:main . -f
# docker run -it --rm -e GITHUB_WORKSPACE=/mnt -v $PWD:/mnt freedwu/translate-shell:main
FROM python

LABEL org.opencontainers.image.title=translate-shell
LABEL org.opencontainers.image.authors="Wu Zhenyu"
LABEL org.opencontainers.image.vendor="Wu Zhenyu"
LABEL org.opencontainers.image.url=https://ghcr.io/Freed-Wu/translate-shell
# https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#labelling-container-images
LABEL org.opencontainers.image.source=https://github.com/Freed-Wu/translate-shell
LABEL org.opencontainers.image.description="Translate .po of one repo"
LABEL org.opencontainers.image.licenses=GPL-3.0

RUN pip install 'translate_shell[po]'

ENTRYPOINT ["python", "-m", "translate_shell.tools.po"]

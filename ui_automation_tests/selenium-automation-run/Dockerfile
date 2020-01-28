FROM python:3.7-stretch AS selenium_base

RUN apt-get update && apt-get install -yq \
    git-core \
    xvfb \
    xsel \
    unzip \
    python-pytest \
    libgconf2-4 \
    libncurses5 \
    libxml2-dev \
    libxslt-dev \
    libz-dev \
    python-pytest-xdist \
    xclip

RUN wget -q "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -O /tmp/google-chrome-stable_current_amd64.deb \
    && apt-get install -f /tmp/google-chrome-stable_current_amd64.deb -yq

# chromeDriver v2.35
RUN wget -q "https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip -o /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip

# xvfb - X server display
COPY xvfb-chrome /usr/bin/xvfb-chrome
RUN rm /usr/bin/google-chrome \
    && ln -s /usr/bin/xvfb-chrome /usr/bin/google-chrome \
    && chmod 777 /usr/bin/xvfb-chrome

FROM selenium_base

# pip
COPY ./e2e.txt /tmp/e2e.txt
RUN pip install -r /tmp/e2e.txt
RUN easy_install -U setuptools
RUN pip install pytest-dependency

# Docker entry
COPY ./docker-entry.sh /
ENTRYPOINT ["/docker-entry.sh"]

CMD ["/bin/true"]

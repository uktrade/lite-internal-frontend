FROM python:3.7-stretch AS selenium_base

RUN apt-get update && apt-get install -yq \
    git-core \
    xvfb=2:1.19.2-1+deb9u5 \
    xsel=1.2.0-2+b1 \
    unzip \
    python-pytest=3.0.6-1 \
    libgconf2-4=3.2.6-4+b1 \
    libncurses5=6.0+20161126-1+deb9u2 \
    libxml2-dev=2.9.4+dfsg1-2.2+deb9u2 \
    libxslt-dev \
    libz-dev \
    python-pytest-xdist \
    xclip=0.12+svn84-4+b1

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    && sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
    && sudo apt-get update
    && sudo apt-get install google-chrome-stable


# xvfb - X server display
COPY google-chrome-stable /usr/bin/google-chrome-stable
RUN ln -s /usr/bin/google-chrome-stable /usr/bin/google-chrome-stable \
    && chmod 777 /usr/bin/google-chrome-stable

# create symlinks to chromedriver and geckodriver (to the PATH)
RUN ln -s /usr/bin/chromium-browser \
    && chmod 777 /usr/bin/google-chrome-stable

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

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 
FROM oven/bun:slim
RUN apt update && apt install git gcc make -y
RUN git clone --depth=1 https://github.com/TinyCC/tinycc.git tinycc
RUN cd tinycc && ./configure --prefix=/usr && make && make install

RUN useradd -ms /bin/bash ctf

COPY src /home/ctf/app
WORKDIR /home/ctf/app
COPY flag /flag
RUN chown -R ctf:ctf * && chown ctf:ctf /tmp

USER ctf
ENV NODE_ENV=production
CMD ["bun", "index.js"]

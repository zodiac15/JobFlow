#!/bin/bash
set -e

apt-get update
apt-get install -y docker.io
apt install -y docker-compose-plugin

systemctl enable docker
systemctl start docker

usermod -aG docker ayush || true

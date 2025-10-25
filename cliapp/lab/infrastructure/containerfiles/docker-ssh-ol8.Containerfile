# docker build -t ssh-ol:8.10 -f docker_ol8
FROM oraclelinux:8.10 AS base

RUN yum update && yum install -y openssh-server sudo unzip ncurses lsof glibc-langpack-en procps binutils file hostname && \
  yum clean all && \
  ssh-keygen -A

FROM base
RUN groupadd -g 5000 ansible && \
  useradd -m -u 5000 -g ansible -s /bin/bash ansible && \
  usermod -aG wheel ansible && \
  echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers && \
  mkdir -p /home/ansible/.ssh && \
  chown -R ansible:ansible /home/ansible/.ssh && \
  chmod 700 /home/ansible/.ssh

COPY id_ansible.pub /home/ansible/.ssh/authorized_keys

RUN chown -R ansible:ansible /home/ansible/.ssh/authorized_keys && \
  chmod 600 /home/ansible/.ssh/authorized_keys

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
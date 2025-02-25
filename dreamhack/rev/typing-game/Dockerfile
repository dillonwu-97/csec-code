FROM ubuntu:22.04@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e

ENV user chall
ENV chall_port 31337

RUN apt-get update
RUN apt-get -y install socat

RUN adduser -u 1337 $user

ADD ./deploy/flag /home/$user/flag
ADD ./deploy/dictionary.txt /home/$user/dictionary.txt
ADD ./deploy/$user /home/$user/$user

RUN chown root:$user /home/$user/flag
RUN chown root:$user /home/$user/dictionary.txt
RUN chown root:$user /home/$user/$user

RUN chmod 755 /home/$user/$user
RUN chmod 440 /home/$user/dictionary.txt
RUN chmod 440 /home/$user/flag

WORKDIR /home/$user
USER $user
EXPOSE $chall_port
CMD socat -T 100 TCP-LISTEN:$chall_port,reuseaddr,fork EXEC:/home/$user/$user


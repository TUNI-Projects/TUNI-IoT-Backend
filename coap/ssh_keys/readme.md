# SSH Keys

You should generate ssh_keys here, using the default `ssh_keygen` command. Send the *.pub key to the PI. Private Key will be used to decrypt in this end.

## Command to Generate SSH Key

1. `ssh-keygen -t rsa -f awesome_secret`

This command will generate a ssh key pair `awesome_secret` in the current directory. This project require the file to be in `ssh_keys` directory.
